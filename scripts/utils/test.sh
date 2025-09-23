docker exec -it fastapi-cde bash
python3
>>> from pymongo import MongoClient
>>> client = MongoClient("mongodb://admin:admin@mongo:27017/trustpilot?authSource=admin")
>>> db = client["trustpilot"]
>>> list(db["societe"].find({}, {"_id": 0, "nom": 1}).limit(5))
>>> list(db["avis_trustpilot"].find({}, {"_id": 0, "id_societe": 1, "commentaire": 1}).limit(5))

