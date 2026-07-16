from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.services.log_analyzer import LogAnalyzer

app = FastAPI(
        title="Cloudops AI",
        version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

analyzer = LogAnalyzer()

class AnalyzeRequest(BaseModel):
    log:str

@app.get("/")
def home():
    return FileResponse("static/index.html")
@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    result = analyzer.analyze(request.log)
    return result
