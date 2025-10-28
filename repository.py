from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGO_URL)
print(client.list_database_names())
db = client["sunday-service"] 