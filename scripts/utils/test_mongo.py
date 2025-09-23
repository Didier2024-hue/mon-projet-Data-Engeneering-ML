import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/home/datascientest/cde/.env.api")  # chemin absolu

print("MONGO_DB =", os.getenv("MONGO_DB"))

client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)
db = client[os.getenv("MONGO_DB")]
print(db.list_collection_names())

