from pymongo import MongoClient
import os

# Remplacer 'mongo' par 'localhost' pour tester depuis ton PC
MONGO_URI = "mongodb://admin:admin@localhost:27017/trustpilot?authSource=admin"

client = MongoClient(MONGO_URI)
db = client["trustpilot"]

print(list(db["societe"].find({}, {"_id": 0, "nom": 1}).limit(5)))
print(list(db["avis_trustpilot"].find({}, {"_id": 0, "id_societe": 1, "commentaire": 1}).limit(5)))

