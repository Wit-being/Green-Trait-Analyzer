import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pickle

# Expanded training data with spiritual context
data = {
    "answer": [
        # Empathy: high (spiritual focus)
        "I find joy in serving others selflessly.",
        "Prayer helps me connect with others’ struggles.",
        "I offer love and support to those in need.",
        "Helping my community brings me peace.",
        # Empathy: low
        "I focus only on my own needs.",
        "Others’ struggles don’t concern me.",
        "I avoid helping unless it benefits me.",
        "I’m indifferent to people’s pain.",
        # Narcissism: high
        "I deserve praise for my greatness.",
        "I’m superior and should be admired.",
        "Everyone must recognize my achievements.",
        "I’m the best at everything I do.",
        # Narcissism: low (spiritual humility)
        "Humility guides my actions daily.",
        "I value others’ contributions above mine.",
        "I seek to learn from everyone’s wisdom.",
        "Serving others is my true purpose.",
        # Growth mindset: high
        "I grow through prayer and reflection.",
        "Mistakes teach me to be better.",
        "I embrace challenges to improve myself.",
        "Learning is a lifelong spiritual journey.",
        # Growth mindset: low
        "I give up when things get tough.",
        "My abilities can’t change.",
        "I avoid challenges to stay safe.",
        "Learning isn’t worth my effort.",
        # Emotional maturity: high
        "I resolve conflicts with calm honesty.",
        "I take responsibility for my actions.",
        "Forgiveness is part of my spiritual path.",
        "I stay patient in difficult moments.",
        # Emotional maturity: low
        "I blame others when things go wrong.",
        "I act on impulse without thinking.",
        "I hold grudges and don’t forgive.",
        "I lose my temper easily.",
        # Openness to difference: high
        "I honor all faiths as paths to truth.",
        "Diverse beliefs enrich my spirit.",
        "I learn from others’ unique perspectives.",
        "Unity comes from embracing differences.",
        # Openness to difference: low
        "I judge those with different beliefs.",
        "Other faiths are wrong and inferior.",
        "I reject people who think differently.",
        "I’m closed to new perspectives."
    ],
    "trait": [
        "empathy_high", "empathy_high", "empathy_high", "empathy_high",
        "empathy_low", "empathy_low", "empathy_low", "empathy_low",
        "narcissism_high", "narcissism_high", "narcissism_high",
        "narcissism_high", "narcissism_low", "narcissism_low",
        "narcissism_low", "narcissism_low", "growth_mindset_high",
        "growth_mindset_high", "growth_mindset_high", "growth_mindset_high",
        "growth_mindset_low", "growth_mindset_low", "growth_mindset_low",
        "growth_mindset_low", "emotional_maturity_high",
        "emotional_maturity_high", "emotional_maturity_high",
        "emotional_maturity_high", "emotional_maturity_low",
        "emotional_maturity_low", "emotional_maturity_low",
        "emotional_maturity_low", "openness_to_difference_high",
        "openness_to_difference_high", "openness_to_difference_high",
        "openness_to_difference_high", "openness_to_difference_low",
        "openness_to_difference_low", "openness_to_difference_low",
        "openness_to_difference_low"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Train a model for each trait
traits = [
    "empathy", "narcissism", "growth_mindset", "emotional_maturity",
    "openness_to_difference"
]
models = {}

for trait in traits:
    df[f"{trait}_label"] = df["trait"].apply(
        lambda x: 1
        if f"{trait}_high" in x else (0 if f"{trait}_low" in x else np.nan))
    df_subset = df.dropna(subset=[f"{trait}_label"])

    pipeline = make_pipeline(TfidfVectorizer(max_features=1000),
                             LogisticRegression(C=1.0, max_iter=1000))

    pipeline.fit(df_subset["answer"], df_subset[f"{trait}_label"])
    models[trait] = pipeline

# Save models
with open("ai_engine/trait_models.pkl", "wb") as f:
    pickle.dump(models, f)

print("Models trained and saved to ai_engine/trait_models.pkl")
