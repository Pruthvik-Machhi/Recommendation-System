import numpy as np
from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
model_name = 'distilbert-base-uncased'
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = TFDistilBertForSequenceClassification.from_pretrained('assets/distilbert', num_labels=2)


def predict_sentiment(review_text):
    inputs = tokenizer(review_text, padding=True, truncation=True, return_tensors='tf')
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_label = np.argmax(logits).item()
    sentiment = 'Positive' if predicted_label == 1 else 'Negative'
    return sentiment
