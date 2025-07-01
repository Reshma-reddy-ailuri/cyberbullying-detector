import os
import tweepy
import numpy as np
from dotenv import load_dotenv
from bert_model import BERTClassifier
from mongo_store import save_to_mongo

# Load environment variables from .env
load_dotenv()

# Get Twitter Bearer Token from environment
bearer_token = os.getenv("TWITTER_BEARER")

# Validate token presence
if not bearer_token:
    raise ValueError("❌ Missing TWITTER_BEARER in .env file")

# Initialize Twitter API client
client = tweepy.Client(bearer_token=bearer_token)

# Initialize BERT classifier
model = BERTClassifier()

# Define search query
query = "mental health OR depression OR anxiety OR suicide OR cyberbullying OR bullying -is:retweet lang:en"

print("🔍 Fetching and analyzing tweets...")

try:
    tweets = client.search_recent_tweets(query=query, max_results=10)

    if tweets.data:
        for tweet in tweets.data:
            print(f"\n📝 Tweet: {tweet.text}")

            # Predict with model
            result = model.predict(tweet.text)
            safe_score, toxic_score = result[0] * 100, result[1] * 100

            print(f"✅ Safe: {safe_score:.2f}% | ❌ Toxic: {toxic_score:.2f}%")

            # Save to MongoDB
            save_to_mongo(tweet.text, safe_score, toxic_score)
    else:
        print("⚠️ No tweets found.")
except tweepy.errors.TooManyRequests:
    print("❌ Twitter API rate limit hit. Please wait and try again later.")
except Exception as e:
    print(f"❌ Error occurred: {e}")
