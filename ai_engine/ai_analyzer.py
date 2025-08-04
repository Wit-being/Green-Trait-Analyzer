import re
import json
import sqlite3
from datetime import datetime

# Define keywords for each trait
trait_rules = {
    "empathy": {
        "keywords": ["care", "understand", "listen", "feel for", "sorry", "support", "help", "empathize", "compassion", "kindness"],
        "weight": 10
    },
    "narcissism": {
        "keywords": ["I am the best", "better than", "always right", "perfect", "amazing", "superior"],
        "self_pronoun_weight": 5
    },
    "growth_mindset": {
        "keywords": ["learn", "improve", "grow", "better myself", "mistake", "work on", "challenge", "effort"],
        "weight": 10
    },
    "emotional_maturity": {
        "keywords": ["reflect", "calm", "responsibility", "apologize", "process", "think through", "accept"],
        "weight": 10
    },
    "openness_to_difference": {
        "keywords": ["respect", "open to", "different beliefs", "diverse", "accept", "understand other", "tolerance"],
        "weight": 10
    }
}

# Count self-focused pronouns for narcissism
def count_self_pronouns(text):
    pronouns = len(re.findall(r'\b(I|me|my|mine)\b', text, re.IGNORECASE))
    return pronouns

# Analyze a single answer
def analyze_answer(answer):
    trait_scores = {}
    for trait, rules in trait_rules.items():
        score = 0
        keyword_count = sum(1 for keyword in rules["keywords"] if keyword.lower() in answer.lower())
        score += keyword_count * rules.get("weight", 0)
        if trait == "narcissism":
            score += count_self_pronouns(answer) * rules.get("self_pronoun_weight", 0)
        trait_scores[trait] = min(round(score, 2), 100)
    return trait_scores

# Analyze all 8 answers and save to database
def analyze_user_answers(user_id, answers):
    if len(answers) != 8:
        return {"error": "Please provide exactly 8 answers"}
    
    final_scores = {trait: 0 for trait in trait_rules}
    for answer in answers:
        scores = analyze_answer(answer)
        for trait, score in scores.items():
            final_scores[trait] += score / 8
    
    for trait in final_scores:
        final_scores[trait] = round(final_scores[trait], 2)
    
    # Save to SQLite database
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
            timestamp TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO user_traits (user_id, empathy, narcissism, growth_mindset, emotional_maturity, openness_to_difference, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        final_scores["empathy"],
        final_scores["narcissism"],
        final_scores["growth_mindset"],
        final_scores["emotional_maturity"],
        final_scores["openness_to_difference"],
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    
    # Save to JSON for easy access
    with open("ai_engine/trait_profile.json", "w") as f:
        json.dump(final_scores, f, indent=2)
    
    return final_scores

# Sample usage
if __name__ == "__main__":
    sample_answers = [
        "Spirituality is my guide. I pray when I’m sad.",
        "I’m learning to be kinder every day.",
        "Connection is sharing true feelings.",
        "Love is a warm, steady bond.",
        "I’d talk openly, not hide.",
        "I’d teach respect for all beliefs.",
        "Soul alignment is shared harmony.",
        "I apologized and listened when I hurt someone."
    ]
    results = analyze_user_answers("user_123", sample_answers)
    print(json.dumps(results, indent=2))
