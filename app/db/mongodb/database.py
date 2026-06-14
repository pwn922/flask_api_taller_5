from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import ActiveConfig


class MongoNotConnectedError(RuntimeError):
    def __init__(self):
        super().__init__("MongoDB connection has not been initialized")


class MongoDBConnection:
    _client: AsyncIOMotorClient | None = None
    _db: AsyncIOMotorDatabase | None = None

    @classmethod
    async def connect(cls):
        if cls._client is None:
            cls._client = AsyncIOMotorClient(ActiveConfig.MONGO_URL)
            cls._db = cls._client[ActiveConfig.MONGO_DB_NAME]

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        if cls._db is None:
            raise MongoNotConnectedError
        return cls._db

    @classmethod
    async def close(cls):
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None
