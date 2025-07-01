import os
from pymongo import MongoClient
from dotenv import load_dotenv
import streamlit as st  # ✅ Required for reading secrets on Streamlit Cloud

# ✅ Load from .env (for local use)
load_dotenv()

# ✅ First try env, then try Streamlit secrets
mongo_uri = os.getenv("MONGO_URI") or st.secrets.get("MONGO_URI")
print("🔍 Loaded MONGO_URI:", mongo_uri)

if not mongo_uri:
    raise ValueError("❌ MONGO_URI not found in .env or Streamlit secrets")

# ✅ Connect to MongoDB
try:
    client = MongoClient(mongo_uri)
    db = client["cyberbullying_db"]
    collection = db["tweets"]
except Exception as e:
    raise ConnectionError(f"❌ Failed to connect to MongoDB: {e}")

# ✅ Save document function
def save_to_mongo(tweet, safe_score, toxic_score):
    document = {
        "text": str(tweet),
        "safe_score": float(safe_score),
        "toxic_score": float(toxic_score)
    }
    collection.insert_one(document)
