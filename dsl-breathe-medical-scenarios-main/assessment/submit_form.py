import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient

load_dotenv(override=True)

client = MongoClient(os.getenv("DATABASE_URI"))

def submit_scenario(scenario, feedback, personal_information):
    client.feedback[os.getenv('FEEDBACK_COLLECTION')].insert_one({
        "scenario": scenario,
        "feedback": feedback,
        "personal_information": personal_information
    })