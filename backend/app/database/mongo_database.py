from ..core.config import settings
from pymongo import MongoClient

client = MongoClient(settings.MONGO_URI)
datasets_db = client[settings.MONGO_DB]