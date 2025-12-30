from flask import Flask, request, jsonify, send_file
from textblob import TextBlob
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Serve the static HTML file
    try:
        return send_file(os.path.join(os.path.dirname(__file__), 'templates/index.html'))
    except Exception as e:
        return f"Error serving file: {str(e)}", 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Fallback to TextBlob for detailed breakdown
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Determine Vibe
        if polarity > 0.1:
            vibe = "Good Vibes"
            emoji = "🌊"
            color = "text-green-400"
        elif polarity < -0.1:
            vibe = "Bad Vibes"
            emoji = "🥀"
            color = "text-red-400"
        else:
            vibe = "Neutral Vibes"
            emoji = "😐"
            color = "text-gray-400"
        
        # Simulate VADER keys for frontend compatibility
        # Pos/Neg/Neu are estimated from polarity
        if polarity > 0:
            pos = polarity * 100
            neg = 0
            neu = 100 - pos
        elif polarity < 0:
            neg = abs(polarity) * 100
            pos = 0
            neu = 100 - neg
        else:
            neu = 100
            pos = 0
            neg = 0

        return jsonify({
            'vibe': vibe,
            'emoji': emoji,
            'color': color,
            'score': round(polarity, 2),
            'breakdown': {
                'pos': round(pos, 1),
                'neu': round(neu, 1),
                'neg': round(neg, 1)
            }
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

# Vercel WSGI entrypoint
if __name__ == '__main__':
    app.run()
