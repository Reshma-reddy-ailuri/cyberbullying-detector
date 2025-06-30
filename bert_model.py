from transformers import BertTokenizer, BertForSequenceClassification
import torch

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
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return probs.detach().cpu().numpy()[0]
