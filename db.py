from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.cve_database
cves_collection = db.cves
