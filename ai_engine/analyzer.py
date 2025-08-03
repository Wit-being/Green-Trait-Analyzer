import re

def analyze_traits(text: str) -> dict:
    text = text.lower()

    traits = {
        "empathy": bool(re.search(r"\bi listened\b|\bi felt\b|\bhe/she felt\b", text)),
        "narcissism": bool(re.search(r"\bi always win\b|\beveryone is beneath me\b", text)),
        "growth_mindset": bool(re.search(r"\bi learned\b|\bi improved\b|\bnext time\b", text)),
        "emotional_depth": bool(re.search(r"\bi cried\b|\bit hurt\b|\bi reflected\b", text))
    }

    return traits
