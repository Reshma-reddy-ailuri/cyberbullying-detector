# dashboard.py
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Load Mongo URI
try:
    mongo_uri = os.getenv("MONGO_URI") or st.secrets["MONGO_URI"]
except:
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    st.error("❌ MONGO_URI not found.")
    st.stop()

client = MongoClient(mongo_uri)
db = client["cyberbullying_db"]
collection = db["tweets"]

# Load data
tweets = list(collection.find())
df = pd.DataFrame(tweets)

# Streamlit layout
st.set_page_config(page_title="Tweet Dashboard", layout="wide")
st.title("📊 Stored Tweets Dashboard")

if not df.empty:
    df = df[['text', 'safe_score', 'toxic_score']]

    # Filter by keyword
    keyword = st.text_input("🔍 Search tweets by keyword:")
    if keyword:
        df = df[df['text'].str.contains(keyword, case=False, na=False)]

    # Sort by toxic score
    sort_by = st.selectbox("📌 Sort by", ["safe_score", "toxic_score"])
    df = df.sort_values(by=sort_by, ascending=False)

    # Download button
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Download as CSV", csv, "tweets.csv", "text/csv")

    # Show table
    st.dataframe(df.style.format({"safe_score": "{:.2f}", "toxic_score": "{:.2f}"}))

    # Summary chart
    st.subheader("📈 Toxicity Distribution")
    st.bar_chart(df[['safe_score', 'toxic_score']])

    # Word Cloud for Toxic Tweets
    st.subheader("🌪️ Word Cloud of Toxic Tweets")
    toxic_texts = df[df['toxic_score'] > 30]['text']

    if not toxic_texts.empty:
        combined_text = " ".join(toxic_texts)
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(combined_text)

        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("Not enough toxic tweets yet to generate a word cloud.")
else:
    st.warning("⚠️ No tweets found in the database yet.")
