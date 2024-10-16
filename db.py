from pymongo import MongoClient
import os

_DATABASE_CONNECTION_STR = os.getenv("DATABASE_CONNECTION_STR")

if not _DATABASE_CONNECTION_STR:
    raise ValueError("DATABASE_CONNECTION_STR environment variable is not set")

client = MongoClient(_DATABASE_CONNECTION_STR)
db = client.cve_database
cves_collection = db.cves
users_collection = db.users
