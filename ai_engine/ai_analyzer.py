import pickle
import json
import sqlite3
from datetime import datetime

# Load trained models
with open("ai_engine/trait_models.pkl", "rb") as f:
    models = pickle.load(f)

# Analyze 8 answers
def analyze_user_answers(user_id, answers):
    if len(answers) != 8:
        return {"error": "Please provide exactly 8 answers"}
    
    final_scores = {}
    for trait, model in models.items():
        # Predict probability of "high" trait for each answer
        probabilities = model.predict_proba(answers)[:, 1]  # Probability of "high"
        # Average and scale to 0-100
        final_scores[trait] = round(float(np.mean(probabilities) * 100), 2)
    
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
        "Spirituality brings calm; I meditate to find peace.",
        "Learning to understand others is my daily goal.",
        "Connection grows when we share honest dreams.",
        "Love is a deep, spiritual bond built on trust.",
        "Honest talks prevent misunderstandings.",
        "Respecting all beliefs fosters unity.",
        "Soulmates share a harmonious vibe.",
        "Apologizing sincerely heals friendships."
    ]
    results = analyze_user_answers("test_user_001", sample_answers)
    print(json.dumps(results, indent=2))
