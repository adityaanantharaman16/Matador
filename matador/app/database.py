# matador/app/database.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI
from contextlib import asynccontextmanager

class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None
        self.db_name = "Matador"
        self.MONGODB_URL = "mongodb+srv://nirajnad:MatadorDatabase@cluster0.cnaa3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    async def connect_to_database(self):
        """Create database connection."""
        try:
            self.client = AsyncIOMotorClient(self.MONGODB_URL)
            self.db = self.client[self.db_name]
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")

            # Setup indexes after connection
            await self.setup_indexes()
        except Exception as e:
            print(f"Could not connect to MongoDB: {e}")
            raise

    async def setup_indexes(self):
        """Setup indexes for efficient score-based queries."""
        try:
            # Indexes for stock pitches
            await self.db.stockpitch.create_index([
                ('score.total_score', -1),
                ('createdAt', -1)
            ])
            await self.db.stockpitch.create_index([
                ('user', 1),
                ('score.total_score', -1)
            ])

            # Indexes for crypto pitches
            await self.db.cryptopitch.create_index([
                ('score.total_score', -1),
                ('createdAt', -1)
            ])
            await self.db.cryptopitch.create_index([
                ('user', 1),
                ('score.total_score', -1)
            ])

            print("Successfully created scoring indexes!")
        except Exception as e:
            print(f"Error creating indexes: {str(e)}")
            raise

    async def close_database_connection(self):
        """Close database connection."""
        if self.client is not None:
            self.client.close()
            print("MongoDB connection closed.")

    def get_collection(self, collection_name: str):
        """Get a specific collection from the database."""
        return self.db[collection_name]

# Create a database instance
db = Database()

# Lifespan context manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    await db.connect_to_database()
    yield
    # Shutdown: Close the database connection
    await db.close_database_connection()

# Create FastAPI instance with lifespan
app = FastAPI(lifespan=lifespan)