from fastapi import FastAPI
from pydantic import BaseModel

from backend.services.log_analyzer import LogAnalyzer

app = FastAPI(
        title="Cloudops AI",
        version="1.0.0"
)

analyzer = LogAnalyzer()

class AnalyzeRequest(BaseModel):
    log:str

@app.get("/")
def home():
    return{
        "message": "Cloudops AI API is running"
    }
@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    result = analyzer.analyze(request.log)
    return result