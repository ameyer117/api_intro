from pymongo import MongoClient

client = MongoClient("mongodb+srv://11meyal:b6671e97-b939-4e89-89a6-ec57d0eb2b27@cluster0.lx4tyrq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.cve_database
cves_collection = db.cves
