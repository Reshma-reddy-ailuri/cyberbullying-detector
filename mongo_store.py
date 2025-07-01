import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from .env
mongo_uri = os.getenv("MONGO_URI")

# Validate presence
if not mongo_uri:
    raise ValueError("❌ MONGO_URI not found in .env file")

# Connect to MongoDB Atlas
try:
    client = MongoClient(mongo_uri)
    db = client["cyberbullying_db"]
    collection = db["tweets"]
except Exception as e:
    raise ConnectionError(f"❌ Failed to connect to MongoDB: {e}")

# Function to save tweet
def save_to_mongo(tweet, safe_score, toxic_score):
    document = {
        "text": str(tweet),
        "safe_score": float(safe_score),
        "toxic_score": float(toxic_score)
    }
    collection.insert_one(document)
