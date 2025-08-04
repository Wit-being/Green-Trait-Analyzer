# Green Trait Analyzer

A machine learning-based analyzer for the Green spiritual dating app. Scores traits (empathy, narcissism, growth mindset, emotional maturity, openness to difference) from 8 onboarding questions using a locally trained model.

## Structure
- `ai_engine/train_model.py`: Trains ML models.
- `ai_engine/ai_analyzer.py`: Analyzes answers.
- `ai_engine/trait_models.pkl`: Trained model file (generated).
- `ai_engine/trait_profile.json`: Output scores (generated).
- `green_users.db`: SQLite database for user data.
- `requirements.txt`: Lists scikit-learn, pandas, numpy.
- `.gitignore`: Ignores temporary files.

## How to Run
1. Import to Replit.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run `train_model.py` to create `trait_models.pkl`.
4. Create `.replit` with `run = "python ai_engine/ai_analyzer.py"`.
5. Run to see scores for sample answers.
