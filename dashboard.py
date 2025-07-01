import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load MongoDB URI from secrets
MONGO_URI = st.secrets["MONGO_URI"]

# Page settings
st.set_page_config(page_title="Tweet Dashboard", layout="wide")
st.title("📊 Stored Tweets Dashboard")

try:
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI, tls=True)
    db = client["cyberbullying_db"]
    collection = db["tweets"]
    tweets = list(collection.find())
    df = pd.DataFrame(tweets)

    if not df.empty:
        df = df[['text', 'safe_score', 'toxic_score']]

        # Keyword filter
        keyword = st.text_input("🔍 Search tweets by keyword:")
        if keyword:
            df = df[df['text'].str.contains(keyword, case=False, na=False)]

        # Sorting
        sort_by = st.selectbox("📌 Sort by", ["safe_score", "toxic_score"])
        df = df.sort_values(by=sort_by, ascending=False)

        # Download CSV
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download as CSV", csv, "tweets.csv", "text/csv")

        # Display table
        st.dataframe(df.style.format({"safe_score": "{:.2f}", "toxic_score": "{:.2f}"}))

        # Bar chart
        st.subheader("📈 Toxicity Distribution")
        st.bar_chart(df[['safe_score', 'toxic_score']])

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
            st.info("ℹ️ Not enough toxic tweets yet to generate a word cloud.")

    else:
        st.warning("⚠️ No tweets found in the database.")

except Exception as e:
    st.error(f"❌ Failed to connect to MongoDB: {e}")
