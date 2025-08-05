import pickle
import json
import sqlite3
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime

# Download VADER lexicon (run once)
nltk.download('vader_lexicon')

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Load trained models
with open("ai_engine/trait_models.pkl", "rb") as f:
    models = pickle.load(f)

# Analyze 8 answers
def analyze_user_answers(user_id, answers):
    if len(answers) != 8:
        return {"error": "Please provide exactly 8 answers"}

    final_scores = {}
    for trait, model in models.items():
        probabilities = model.predict_proba(answers)[:, 1]  # Probability of "high"
        # Adjust scores with sentiment
        sentiment_scores = [sid.polarity_scores(answer)['compound'] for answer in answers]
        adjusted_probs = [
            prob * (1 + 0.2 * sent)  # Boost for positive sentiment, reduce for negative
            for prob, sent in zip(probabilities, sentiment_scores)
        ]
        final_scores[trait] = round(float(np.mean(adjusted_probs) * 100), 2)
        final_scores[trait] = max(0, min(final_scores[trait], 100))  # Cap at 0-100

    # Save to SQLite
    conn = sqlite3.connect("green_users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_traits (
            user_id TEXT,
            empathy REAL,
            narcissism REAL,
            growth_mindset REAL,
            emotional_maturity REAL,
            openness_to_difference REAL,
            answers TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO user_traits (user_id, empathy, narcissism, growth_mindset, emotional_maturity, openness_to_difference, answers, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        final_scores["empathy"],
        final_scores["narcissism"],
        final_scores["growth_mindset"],
        final_scores["emotional_maturity"],
        final_scores["openness_to_difference"],
        json.dumps(answers),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

    # Save to JSON
    with open("ai_engine/trait_profile.json", "w") as f:
        json.dump(final_scores, f, indent=2)

    return final_scores

# Sample usage
if __name__ == "__main__":
    sample_answers = [
        "Prayer and helping others bring me peace.",
        "I work daily to be more compassionate.",
        "Connection means sharing spiritual dreams.",
        "Love is about mutual growth and trust.",
        "I talk openly to resolve conflicts.",
        "Respecting all faiths builds community.",
        "Soulmates share a spiritual harmony.",
        "I apologized and learned from my errors."
    ]
    results = analyze_user_answers("test_user_002", sample_answers)
    print(json.dumps(results, indent=2))
