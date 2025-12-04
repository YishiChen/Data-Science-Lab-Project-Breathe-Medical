import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient

load_dotenv(override=True)

client = MongoClient(os.getenv("DATABASE_URI"))

def fetch_results():
    results = client.feedback[os.getenv('FEEDBACK_COLLECTION')].find({})

    return list(results)