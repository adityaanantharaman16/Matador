# matador/app/crud.py
from typing import Optional, List
from bson import ObjectId
from fastapi import HTTPException
from database import db

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

# Create CRUD instances for each collection
# Users will use string IDs
users_crud = CRUD('user')
users_crud.use_object_id = False  # Users will use string IDs

# Other collections will use ObjectIds
stocks_crud = CRUD('stock')
crypto_crud = CRUD('crypto')
stock_pitches_crud = CRUD('stockpitch')
crypto_pitches_crud = CRUD('cryptopitch')
comments_crud = CRUD('comment')