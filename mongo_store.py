import os
from pymongo import MongoClient
from dotenv import load_dotenv

# ✅ Use streamlit only when running on Streamlit Cloud
try:
    import streamlit as st
    mongo_uri = os.getenv("MONGO_URI") or st.secrets["MONGO_URI"]
except ImportError:
    # Not running in Streamlit Cloud (e.g., local)
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")

print("🔍 Loaded MONGO_URI:", mongo_uri)

if not mongo_uri:
    raise ValueError("❌ MONGO_URI not found in .env or Streamlit secrets")

# ✅ Connect to MongoDB Atlas
try:
    client = MongoClient(mongo_uri)
    db = client["cyberbullying_db"]
    collection = db["tweets"]
except Exception as e:
    raise ConnectionError(f"❌ Failed to connect to MongoDB: {e}")

# ✅ Save tweet data to MongoDB
def save_to_mongo(tweet, safe_score, toxic_score):
    document = {
        "text": str(tweet),
        "safe_score": float(safe_score),
        "toxic_score": float(toxic_score)
    }
    collection.insert_one(document)
