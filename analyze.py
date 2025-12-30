from textblob import TextBlob
import sys

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment

def get_sentiment_label(polarity):
    if polarity > 0.1:
        return "Positive 😊"
    elif polarity < -0.1:
        return "Negative 😠"
    else:
        return "Neutral 😐"

if __name__ == "__main__":
    print("--- Simple Sentiment Analyzer ---")
    
    if len(sys.argv) > 1:
        # Command line argument mode
        text = " ".join(sys.argv[1:])
    else:
        # Interactive mode
        text = input("Enter text to analyze: ")

    if not text.strip():
        print("No text provided.")
        sys.exit(1)

    result = analyze_sentiment(text)
    label = get_sentiment_label(result.polarity)

    print(f"\nAnalyzing: \"{text}\"")
    print(f"Polarity: {result.polarity:.2f} (Scale: -1.0 to 1.0)")
    print(f"Subjectivity: {result.subjectivity:.2f} (Scale: 0.0 to 1.0)")
    print(f"Result: {label}")
