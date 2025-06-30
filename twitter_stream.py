# twitter_stream.py

import os
import tweepy
from bert_model import BERTClassifier
from mongo_store import save_to_mongo

# Load your Bearer Token (store securely in real projects)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALBi2wEAAAAAK7T02CaHR3k%2FkiI2M4GvDNPC25o%3DRwZM4bNLX9bUieff1dmB6kdJa4VFNacDdHwUWkjNsvqnvbqXw0"

# Initialize the Twitter client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Query: Fetch tweets mentioning anxiety, depression, etc.
query = "(anxiety OR depression OR cyberbullying OR sad OR stressed OR lonely OR trauma OR mental health lang:en -is:retweet)"

# Fetch tweets
print("🔍 Fetching and analyzing tweets...\n")
tweets = client.search_recent_tweets(query=query, max_results=10)

model = BERTClassifier()

# Analyze and store each tweet
for tweet in tweets.data:
    text = tweet.text
    safe_score, toxic_score, label = model.predict(text)

    print("📝 Tweet:", text)
    print(f"✅ Safe: {safe_score:.2f}% | ❌ Toxic: {toxic_score:.2f}% | 🏷️ Label: {label}")
    print("-" * 60)

    # Save to MongoDB
    save_to_mongo(text, safe_score, toxic_score, label)
