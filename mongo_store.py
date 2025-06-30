# mongo_store.py

from pymongo import MongoClient

def save_to_mongo(text, safe_score, toxic_score, label):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["cyberbullying_db"]
    collection = db["tweets"]

    document = {
        "text": text,
        "safe_score": float(safe_score),
        "toxic_score": float(toxic_score),
        "label": label
    }

    collection.insert_one(document)
