from fastapi import FastAPI, Body
from pydantic import BaseModel
from ai_engine.analyzer import analyze_traits

app = FastAPI()

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    result = analyze_traits(request.text)
    return {"analysis": result}
