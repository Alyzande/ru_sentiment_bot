from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from flask_cors import CORS  # Important for frontend-backend communication
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # This allows your frontend to talk to the backend
load_dotenv() #load dotenv

# Load the model ONCE when the server starts
print("Loading Russian sentiment model... (this may take a moment)")
model_name = "sismetanin/rubert-ru-sentiment-rusentiment"
classifier = pipeline("sentiment-analysis", model=model_name)
print("Model loaded successfully!")

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    # Get the JSON data from the request
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Get the prediction from our model
        result = classifier(text)[0]
        
        # Map the label to a more readable format
        label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        sentiment = label_map.get(result['label'], result['label'])
        
        return jsonify({
            'sentiment': sentiment,
            'confidence': result['score'],
            'text': text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/russian-news')
def get_russian_news():
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    
    try:
        # Fetch top headlines from Russian news sources
        url = f"https://newsapi.org/v2/everything?q=Россия&language=ru&pageSize=10&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        news_data = response.json()
        
        # Analyze sentiment for each headline
        analyzed_news = []
        for article in news_data.get('articles', []):
            headline = article.get('title', '')
            if headline:
                result = classifier(headline)[0]
                label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
                sentiment = label_map.get(result['label'], result['label'])
                
                analyzed_news.append({
                    'headline': headline,
                    'sentiment': sentiment,
                    'confidence': round(result['score'] * 100, 2),
                    'source': article.get('source', {}).get('name', ''),
                    'url': article.get('url', '')
                })
        
        return jsonify(analyzed_news)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    app.run(debug=True, port=5000)