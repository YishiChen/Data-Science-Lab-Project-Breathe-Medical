import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
import datetime

load_dotenv(override=True)

client = MongoClient(os.getenv("DATABASE_URI"))

def report_error(scenario):
    client.feedback.errors.insert_one({
        "scenario": scenario,
        "timestamp": datetime.datetime.now()
    })