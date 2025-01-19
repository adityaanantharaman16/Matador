# matador/app/crud.py
from typing import Optional, List
from bson import ObjectId
from fastapi import HTTPException
from database import db
from scoring.content_scorer import ContentScorer
from logger import logger


class CRUD:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.use_object_id = True  # Flag to determine ID handling

    @property
    def collection(self):
        return db.get_collection(self.collection_name)

    async def create(self, document: dict) -> dict:
        """Create a new document in the collection."""
        try:
            # If _id is provided in document, use it as is
            if "_id" in document:
                self.use_object_id = False

            result = await self.collection.insert_one(document)
            return await self.get_by_id(str(result.inserted_id))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Create failed: {str(e)}")

    async def get_by_id(self, id: str) -> Optional[dict]:
        """Get a document by its ID."""
        try:
            # Use ObjectId only if use_object_id is True
            query = {"_id": ObjectId(id) if self.use_object_id else id}
            document = await self.collection.find_one(query)
            if document:
                if self.use_object_id:
                    document["_id"] = str(document["_id"])
            return document
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Document not found: {str(e)}")

    async def get_all(self, filter_dict: dict = None, limit: int = 100) -> List[dict]:
        """Get all documents in the collection with optional filtering."""
        cursor = self.collection.find(filter_dict or {}).limit(limit)
        documents = []
        async for document in cursor:
            if self.use_object_id and isinstance(document["_id"], ObjectId):
                document["_id"] = str(document["_id"])
            documents.append(document)
        return documents

    async def update(self, id: str, data: dict) -> Optional[dict]:
        """Update a document by its ID."""
        try:
            query = {"_id": ObjectId(id) if self.use_object_id else id}
            result = await self.collection.update_one(query, {"$set": data})
            if result.modified_count:
                return await self.get_by_id(id)
            raise HTTPException(status_code=404, detail="Document not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

    async def delete(self, id: str) -> bool:
        """Delete a document by its ID."""
        try:
            query = {"_id": ObjectId(id) if self.use_object_id else id}
            result = await self.collection.delete_one(query)
            if result.deleted_count:
                return True
            raise HTTPException(status_code=404, detail="Document not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

class ScoringCRUD(CRUD):
    def __init__(self, collection_name: str):
        super().__init__(collection_name)
        self.content_scorer = ContentScorer()

    async def create_with_score(self, document: dict) -> dict:
        """Create a document and calculate its initial score."""
        # First create the document
        created_doc = await self.create(document)

        # Get user karma for scoring
        user_id = document.get('user')
        user_karma = await users_crud.get_by_id(user_id)

        # Calculate initial score
        score = await self.content_scorer.calculate_pitch_score(
            created_doc,
            user_karma
        )

        # Update document with score
        score_dict = score.model_dump()
        await self.update(str(created_doc['_id']), {
            'score': score_dict
        })

        return await self.get_by_id(str(created_doc['_id']))

    async def update_scores(self, filter_dict: dict = None) -> int:
        """Update scores for multiple documents."""
        cursor = self.collection.find(filter_dict or {})
        update_count = 0

        async for document in cursor:
            try:
                user_karma = await users_crud.get_by_id(document['user'])
                score = await self.content_scorer.calculate_pitch_score(
                    document,
                    user_karma
                )

                await self.update(
                    str(document['_id']),
                    {'score': score.model_dump()}
                )
                update_count += 1
            except Exception as e:
                logger.error(f"Score update failed for {document['_id']}: {str(e)}")

        return update_count

    async def get_top_scored(
            self,
            limit: int = 20,
            skip: int = 0,
            min_score: float = 0
    ) -> List[dict]:
        """Get documents sorted by score."""
        cursor = self.collection.find(
            {'score.total_score': {'$gte': min_score}}
        ).sort(
            'score.total_score', -1
        ).skip(skip).limit(limit)

        return [doc async for doc in cursor]

# Create CRUD instances for each collection
stock_pitches_crud = ScoringCRUD('stockpitch')
crypto_pitches_crud = ScoringCRUD('cryptopitch')

# Users will use string IDs
users_crud = CRUD('user')
users_crud.use_object_id = False  # Users will use string IDs

# Other collections will use ObjectIds
stocks_crud = CRUD('stock')
crypto_crud = CRUD('crypto')
stock_pitches_crud = CRUD('stockpitch')
crypto_pitches_crud = CRUD('cryptopitch')
comments_crud = CRUD('comment')