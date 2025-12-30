from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

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

        # Perform VADER Analysis
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Determine Vibe based on Compound Score
        if compound >= 0.05:
            vibe = "Good Vibes"
            emoji = "🌊"
            color = "text-green-400"
        elif compound <= -0.05:
            vibe = "Bad Vibes"
            emoji = "🥀"
            color = "text-red-400"
        else:
            vibe = "Neutral Vibes"
            emoji = "😐"
            color = "text-gray-400"
            
        return jsonify({
            'vibe': vibe,
            'emoji': emoji,
            'color': color,
            'score': round(compound, 2),
            'breakdown': {
                'pos': round(scores['pos'] * 100, 1),
                'neu': round(scores['neu'] * 100, 1),
                'neg': round(scores['neg'] * 100, 1)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel WSGI entrypoint
if __name__ == '__main__':
    app.run()
