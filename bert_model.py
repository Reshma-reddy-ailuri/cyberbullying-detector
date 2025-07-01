from transformers import BertTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F  # Required for softmax

class BERTClassifier:
    def __init__(self):
        self.model_name = "unitary/toxic-bert"
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name)
        self.model.eval()

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=1)

            # Extract probabilities
            safe_prob = probs[0][0].item()
            toxic_prob = probs[0][1].item()

            # Convert to percentage and round
            safe_score = round(safe_prob * 100, 2)
            toxic_score = round(toxic_prob * 100, 2)

            # Assign label
            if toxic_score > 70:
                label = "🔴 Highly Toxic"
            elif toxic_score > 30:
                label = "🟠 Possibly Toxic"
            else:
                label = "🟢 Safe"

            return safe_score, toxic_score, label
