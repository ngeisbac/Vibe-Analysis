import streamlit as st
from textblob import TextBlob

# Set page config for a cleaner look
st.set_page_config(page_title="Vibe Analysis", page_icon="🌊", layout="centered")

def get_sentiment_label(polarity):
    if polarity > 0.1:
        return "Good Vibes", "🌊"
    elif polarity < -0.1:
        return "Bad Vibes", "🥀"
    else:
        return "Neutral Vibes", "😐"

def main():
    st.title("🌊 Vibe Analysis")
    st.markdown("Check the vibe of your text.")

    # Text Area for User Input
    user_text = st.text_area("Your Text", height=150, placeholder="Type something here to check the vibe...")

    if st.button("Analyze Sentiment", type="primary"):
        if user_text.strip():
            # Perform Analysis
            blob = TextBlob(user_text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            label, emoji = get_sentiment_label(polarity)
            
            # Display Results
            st.markdown("---")
            st.subheader("Analysis Result")
            
            # Use columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Sentiment", label)
            
            with col2:
                st.metric("Polarity", f"{polarity:.2f}")
            
            with col3:
                st.metric("Subjectivity", f"{subjectivity:.2f}")

            # Visual Feedback
            st.success(f"This text is **{label}** {emoji}")
            
            # Expander for extensive details
            with st.expander("What do these numbers mean?"):
                st.write("""
                - **Polarity**: Ranges from -1 (Negative) to +1 (Positive).
                - **Subjectivity**: Ranges from 0 (Objective) to 1 (Subjective/Opinionated).
                """)
        else:
            st.warning("Please enter some text to analyze.")

if __name__ == "__main__":
    main()
