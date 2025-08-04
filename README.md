# AI Engine for Green Trait Analyzer

This folder contains the core AI logic for analyzing user answers in the Green spiritual dating app.

## Files
- `ai_analyzer.py`: Analyzes answers to 8 questions to score traits like empathy, narcissism, growth mindset, emotional maturity, and openness to difference.
- `trait_model.pkl`: Placeholder for a future trained model (not used currently).
- `trait_profile.json`: Output file with trait scores (generated when running `ai_analyzer.py`).

## How It Works
- Uses Hugging Face's `transformers` library for sentiment analysis.
- Scores traits based on keywords and sentiment in user answers.
- Run `ai_analyzer.py` to test with sample answers.
