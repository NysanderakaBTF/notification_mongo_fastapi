from motor.motor_asyncio import AsyncIOMotorClient

from core.config.env_config import config

client = AsyncIOMotorClient(config.DB_URI)

db = client.notifications
test_db = client.tests

user_collection = db.get_collection('user_collection')
test_collection = db.get_collection('test_collection')
