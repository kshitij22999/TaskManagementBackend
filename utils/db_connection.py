from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()

url = os.getenv('MONGODB_URI')

def get_db():
    client = MongoClient(url,server_api=ServerApi('1'))
    db = client["task_management"]
    return db