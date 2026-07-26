from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

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
    try:
        result = analyzer.analyze(request.log)

        return JSONResponse(
            status_code=200,
            content=result
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "source": "CloudOps_AI",
                "error_type": "internal_server_error",
                "message": "An unexpected error occurred while analyzing the log."
            }
        )
