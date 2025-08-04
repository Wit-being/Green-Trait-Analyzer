# Green Trait Analyzer

A lightweight analyzer for the Green spiritual dating app. Scores traits (empathy, narcissism, growth mindset, emotional maturity, openness to difference) from 8 onboarding questions using keyword matching.

## Structure
- `ai_engine/ai_analyzer.py`: Main analyzer script.
- `ai_engine/trait_profile.json`: Output scores (generated).
- `green_users.db`: SQLite database for user scores.
- `requirements.txt`: No external libraries needed.
- `.gitignore`: Ignores temporary files.

## How to Run
1. Import to Replit.
2. Create `.replit` with `run = "python ai_engine/ai_analyzer.py"`.
3. Run to see scores for sample answers.
