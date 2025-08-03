import spacy

# Load small English model
nlp = spacy.load("en_core_web_sm")

# Define trait patterns
TRAIT_KEYWORDS = {
    "empathy": ["understand", "feel with", "compassion", "listen", "care"],
    "narcissism": ["better than", "deserve", "superior", "admire me", "only one"],
    "growth_mindset": ["learn", "improve", "challenge", "get better", "fail and grow"],
    "humility": ["I was wrong", "I learned", "changed my mind", "they were right"],
}

def analyze_text(text: str) -> dict:
    doc = nlp(text.lower())
    trait_scores = {}

    for trait, patterns in TRAIT_KEYWORDS.items():
        score = 0
        for token in doc:
            for pattern in patterns:
                if pattern in token.text or pattern in token.sent.text:
                    score += 1
        trait_scores[trait] = score

    return trait_scores
