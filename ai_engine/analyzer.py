# Import libraries for NLP and text processing
from transformers import pipeline
import re
import json

# Initialize Hugging Face sentiment analysis model (distilbert for simplicity)
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Define keywords and rules for each trait
trait_rules = {
    "empathy": {
        "keywords": ["care", "understand", "listen", "feel for", "sorry", "support", "help", "empathize"],
        "positive_sentiment_weight": 0.7,  # Positive sentiment boosts empathy score
        "keyword_weight": 0.3  # Keywords add to the score
    },
    "narcissism": {
        "keywords": ["I am the best", "better than", "always right", "perfect", "amazing", "superior"],
        "self_pronoun_weight": 0.5,  # High use of "I" increases narcissism score
        "keyword_weight": 0.5
    },
    "growth_mindset": {
        "keywords": ["learn", "improve", "grow", "better myself", "mistake", "work on", "challenge"],
        "positive_sentiment_weight": 0.6,
        "keyword_weight": 0.4
    },
    "emotional_maturity": {
        "keywords": ["reflect", "calm", "responsibility", "apologize", "process", "think through"],
        "positive_sentiment_weight": 0.7,
        "keyword_weight": 0.3
    },
    "openness_to_difference": {
        "keywords": ["respect", "open to", "different beliefs", "diverse", "accept", "understand other"],
        "positive_sentiment_weight": 0.6,
        "keyword_weight": 0.4
    }
}

# Function to count self-focused pronouns (for narcissism)
def count_self_pronouns(text):
    pronouns = len(re.findall(r'\b(I|me|my|mine)\b', text, re.IGNORECASE))
    return pronouns / len(text.split()) if text.split() else 0  # Normalize by word count

# Function to analyze a single answer
def analyze_answer(answer):
    # Get sentiment (positive/negative) and score from Hugging Face model
    sentiment_result = sentiment_analyzer(answer)[0]
    sentiment = sentiment_result['label']
    sentiment_score = sentiment_result['score']
    
    # Initialize trait scores
    trait_scores = {}
    
    # Analyze each trait
    for trait, rules in trait_rules.items():
        score = 0
        
        # Check for keywords
        keyword_count = sum(1 for keyword in rules["keywords"] if keyword.lower() in answer.lower())
        keyword_score = min(keyword_count * 10, 30) * rules.get("keyword_weight", 0)  # Max 30 points from keywords
        
        # Add sentiment contribution
        if sentiment == "POSITIVE":
            sentiment_contribution = sentiment_score * 100 * rules.get("positive_sentiment_weight", 0)
        else:
            sentiment_contribution = (1 - sentiment_score) * 50 * rules.get("positive_sentiment_weight", 0)  # Negative sentiment lowers score
        
        # Special case for narcissism: count self-pronouns
        if trait == "narcissism":
            pronoun_score = count_self_pronouns(answer) * 100 * rules.get("self_pronoun_weight", 0)
            score = min(keyword_score + pronoun_score, 100)
        else:
            score = min(keyword_score + sentiment_contribution, 100)
        
        trait_scores[trait] = round(score, 2)
    
    return trait_scores

# Function to analyze all 8 answers and combine scores
def analyze_user_answers(answers):
    if len(answers) != 8:
        return {"error": "Please provide exactly 8 answers"}
    
    # Initialize final scores
    final_scores = {trait: 0 for trait in trait_rules}
    
    # Analyze each answer
    for answer in answers:
        scores = analyze_answer(answer)
        for trait, score in scores.items():
            final_scores[trait] += score / 8  # Average across 8 questions
    
    # Round final scores
    for trait in final_scores:
        final_scores[trait] = round(final_scores[trait], 2)
    
    return final_scores

# Example usage with sample answers
sample_answers = [
    "I think spirituality is personal. When I’m down, I talk to friends and reflect.",  # Q1
    "I’ve been learning to be more patient lately. It’s tough but rewarding.",  # Q2
    "I know I’ve connected when we share deep conversations and laugh together.",  # Q3
    "I zinged once and it felt like my heart opened up. Love should feel free.",  # Q4
    "If I were you, I’d reach out and be honest, not disappear.",  # Q5
    "As president, I’d encourage people to learn about different faiths and cultures.",  # Q6
    "I believe in soulful alignment—it’s like your hearts vibe together.",  # Q7
    "I hurt a friend once, felt awful, and apologized to make it right."  # Q8
]

# Run analysis and print results
if __name__ == "__main__":
    results = analyze_user_answers(sample_answers)
    print(json.dumps(results, indent=2))
    
    # Save results to a file
    with open("trait_profile.json", "w") as f:
        json.dump(results, f, indent=2)
