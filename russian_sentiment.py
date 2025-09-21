# russian_sentiment.py
from transformers import pipeline

# Tell the pipeline to use the specific Russian model you found
model_name = "sismetanin/rubert-ru-sentiment-rusentiment"
classifier = pipeline("sentiment-analysis", model=model_name)

# Your Russian text
russian_text = "Это прекрасный день. Я учусь программировать."

print("Sending text to the Russian model...")
result = classifier(russian_text)[0]  # Get the first result

print(f"\nText: {russian_text}")
print(f"Sentiment: {result['label']}")
print(f"Confidence: {result['score']:.4f}")