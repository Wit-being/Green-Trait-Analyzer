from fastapi import FastAPI, Request
from ai_engine.analyzer import analyze_text

app = FastAPI()

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    text = data.get("text", "")
    result = analyze_text(text)
    return result
