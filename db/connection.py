import os
import certifi

from pymongo import MongoClient
from dotenv import load_dotenv

ca = certifi.where()
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI, tlsCAFile=ca)

for db in client.list_database_names():
    print(db)