from motor.motor_asyncio import AsyncIOMotorClient

from core.config.env_config import config

client = AsyncIOMotorClient(config.DB_URI)

db = client.notifications

user_collection = db.get_collection('user_collection')
