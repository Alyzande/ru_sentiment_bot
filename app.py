# app.py
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from flask_cors import CORS  # Important for frontend-backend communication

app = Flask(__name__, static_folder='styles')
CORS(app)  # This allows your frontend to talk to the backend

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    app.run(debug=True, port=5000)