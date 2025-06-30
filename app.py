import streamlit as st
from bert_model import BERTClassifier

st.set_page_config(page_title="Cyberbullying Detector", layout="centered")

st.title("🤖 AI-Powered Cyberbullying & Mental Health Detector")
st.markdown("Detect toxic or cyberbullying content in social media posts using a fine-tuned BERT model.")

model = BERTClassifier()

text = st.text_area("Paste a social media post here:", height=150)

if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing..."):
            result = model.predict(text)
        st.success("Analysis Complete!")
        st.write(f"🟢 Safe Content Probability: {result[0]*100:.2f}%")
        st.write(f"🔴 Cyberbullying/Toxic Content Probability: {result[1]*100:.2f}%")
