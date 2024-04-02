import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import sys

# from dotenv import load_dotenv

# load_dotenv()

logger = logging.getLogger("subject-service")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

uri = "mongodb+srv://milanjobemail:<SWNs7bviE18NSBEGPUiN4rcry23H3h0oh8fOHX4dTWyCWxdKKUQC4AvViwcabKcl>@clustersongs.dcnpopi.mongodb.net/?retryWrites=true&w=majority"

# client = MongoClient(os.getenv('DATABASE_URL', "mongodb://localhost:27018"))
client = MongoClient(uri, server_api=ServerApi('1'))
# db_name = os.getenv('DATABASE_NAME', "local")
db_name = "sunday-service"

try:
    client.admin.command('ping')
    logger.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logger.info(e)

dblist = client.list_database_names()
if db_name in dblist:
  logger.info("Database connected successfully")

db = client[db_name]