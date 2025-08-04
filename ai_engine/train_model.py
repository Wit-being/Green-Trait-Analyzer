import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pickle
import json

# Synthetic training data (simulating answers with labeled traits)
data = {
    "answer": [
        # Empathy: high
        "I listen and care deeply about others’ feelings.",
        "I always try to understand and help people.",
        # Empathy: low
        "I don’t care about others’ problems.",
        "People should handle their own issues.",
        # Narcissism: high
        "I’m the best and everyone should admire me.",
        "I’m always right and superior to others.",
        # Narcissism: low
        "I value teamwork and others’ input.",
        "I’m humble and learn from others.",
        # Growth mindset: high
        "I love learning from my mistakes.",
        "Challenges help me grow and improve.",
        # Growth mindset: low
        "I give up when things get hard.",
        "My skills are fixed and can’t change.",
        # Emotional maturity: high
        "I reflect calmly and take responsibility.",
        "I apologize and think through conflicts.",
        # Emotional maturity: low
        "I get angry and blame others.",
        "I act impulsively without reflection.",
        # Openness to difference: high
        "I respect and learn from diverse beliefs.",
        "I’m open to different perspectives.",
        # Openness to difference: low
        "I judge people with different views.",
        "I’m closed-minded about other beliefs."
    ],
    "trait": [
        "empathy_high", "empathy_high", "empathy_low", "empathy_low",
        "narcissism_high", "narcissism_high", "narcissism_low", "narcissism_low",
        "growth_mindset_high", "growth_mindset_high", "growth_mindset_low", "growth_mindset_low",
        "emotional_maturity_high", "emotional_maturity_high", "emotional_maturity_low", "emotional_maturity_low",
        "openness_to_difference_high", "openness_to_difference_high", "openness_to_difference_low", "openness_to_difference_low"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Train a model for each trait
traits = ["empathy", "narcissism", "growth_mindset", "emotional_maturity", "openness_to_difference"]
models = {}

for trait in traits:
    # Create labels: 1 for high, 0 for low
    df[f"{trait}_label"] = df["trait"].apply(lambda x: 1 if f"{trait}_high" in x else (0 if f"{trait}_low" in x else np.nan))
    df_subset = df.dropna(subset=[f"{trait}_label"])
    
    # Create pipeline: TF-IDF vectorizer + Logistic Regression
    pipeline = make_pipeline(
        TfidfVectorizer(max_features=1000),
        LogisticRegression()
    )
    
    # Train model
    pipeline.fit(df_subset["answer"], df_subset[f"{trait}_label"])
    models[trait] = pipeline

# Save models to file
with open("ai_engine/trait_models.pkl", "wb") as f:
    pickle.dump(models, f)

print("Models trained and saved to ai_engine/trait_models.pkl")
