# app.py
import streamlit as st
import pandas as pd
from bert_model import BERTClassifier
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from mongo_store import save_to_mongo
from pymongo import MongoClient
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

# Initialize BERT model
model = BERTClassifier()

# Set page config
st.set_page_config(page_title="Cyberbullying Detector", layout="wide")
st.title("🤖 AI-Powered Cyberbullying & Mental Health Dashboard")

# Navigation tabs
page = st.sidebar.selectbox("Choose a view:", ["🔍 Live Prediction", "📊 Dashboard"])

# Page 1: Live Prediction
if page == "🔍 Live Prediction":
    st.header("🔍 Detect Toxicity in a Social Media Post")
    st.markdown("Use our fine-tuned BERT model to classify content as safe or toxic.")

    text = st.text_area("Paste a tweet or post here:", height=150)
    if st.button("Analyze"):
        if text.strip() == "":
            st.warning("⚠️ Please enter some text to analyze.")
        else:
            with st.spinner("Analyzing..."):
                result = model.predict(text)
                save_to_mongo(text, result[0], result[1])  # Save to MongoDB
            st.success("✅ Analysis Complete!")
            st.write(f"🟢 Safe Content Probability: {result[0]*100:.2f}%")
            st.write(f"🔴 Cyberbullying/Toxic Content Probability: {result[1]*100:.2f}%")

# Page 2: Dashboard
elif page == "📊 Dashboard":
    st.header("📊 Tweet Analysis Dashboard")

    try:
        tweets = list(collection.find())
        df = pd.DataFrame(tweets)

        if not df.empty:
            df = df[['text', 'safe_score', 'toxic_score']]

            # Filter by keyword
            keyword = st.text_input("🔍 Search tweets by keyword:")
            if keyword:
                df = df[df['text'].str.contains(keyword, case=False, na=False)]

            # Sort by score
            sort_by = st.selectbox("📌 Sort by", ["safe_score", "toxic_score"])
            df = df.sort_values(by=sort_by, ascending=False)

            # Download button
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download as CSV", csv, "tweets.csv", "text/csv")

            # Data table
            st.dataframe(df.style.format({"safe_score": "{:.2f}", "toxic_score": "{:.2f}"}))

            # Word Cloud
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

            # Bar chart
            st.subheader("📈 Toxicity Distribution")
            st.bar_chart(df[['safe_score', 'toxic_score']])
        else:
            st.warning("⚠️ No tweets found in the database yet.")

    except Exception as e:
        st.error(f"❌ Failed to load dashboard: {e}")
