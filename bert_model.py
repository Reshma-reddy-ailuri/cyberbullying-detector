# bert_model.py

from transformers import BertTokenizer, BertForSequenceClassification
import torch

class BERTClassifier:
    def __init__(self):
        self.model_name = "unitary/toxic-bert"
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name)
        self.model.eval()

    def predict(self, text):
        # Tokenize input
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Run through the model without computing gradients
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Convert to standard Python floats
        safe_score = float(probs[0][0]) * 100
        toxic_score = float(probs[0][1]) * 100

        # Add a label based on confidence
        if toxic_score > 70:
            label = "🔴 Highly Toxic"
        elif toxic_score > 30:
            label = "🟠 Possibly Toxic"
        else:
            label = "🟢 Safe"

        return safe_score, toxic_score, label
