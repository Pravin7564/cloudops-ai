from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from backend.rules.candidate_rule_store import CandidateRuleStore
from backend.rules.rule_approval import RuleApproval
from backend.rules.rule_promoter import RulePromoter
from backend.services.log_analyzer import LogAnalyzer

app = FastAPI(
title="Cloudops AI",
version="1.0.0"
)

app.mount(
"/static",
StaticFiles(directory="static"),
name="static"
)

analyzer = LogAnalyzer()
candidate_store = CandidateRuleStore()
rule_approval = RuleApproval()
rule_promoter = RulePromoter()

class AnalyzeRequest(BaseModel):
    log: str

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

    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "source": "CloudOps_AI",
                "error_type": "internal_server_error",
                "message": (
                    "An unexpected error occurred "
                    "while analyzing the log."
                )
            }
        )

@app.get("/rules/candidates")
def list_rule_candidates():
    try:
        candidates = candidate_store._load()
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "count": len(candidates),
                "candidates": candidates
            }
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "source": "CloudOps_AI",
                "error_type": "internal_server_error",
                "message": "Unable to load rule candidates."
            }
        )

@app.get("/rules/candidates/{pattern}")
def get_rule_candidate(pattern: str):
    try:
        candidates = candidate_store._load()

        for candidate in candidates:

            if candidate.get("pattern") == pattern:
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "success",
                        "candidate": candidate
                    }
                )

        return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "error_type": "rule_not_found",
                    "message": (
                        "No rule candidate found "
                        "with this pattern."
                    ),
                "pattern": pattern
                }
        )

    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "source": "CloudOps_AI",
                "error_type": "internal_server_error",
                "message": "Unable to load rule candidate."
            }
        )

@app.post("/rules/candidates/{pattern}/approve")
def approve_rule_candidate(pattern: str):
    try:
        result = rule_approval.approve(pattern)
        if result.get("status") == "success":
            return JSONResponse(
                status_code=200,
                content=result
            )
        if result.get("status") == "already_approved":
            return JSONResponse(
                status_code=200,
                content=result
            )
        if result.get("status") == "not_found":
            return JSONResponse(
                status_code=404,
                content=result
            )
        return JSONResponse(
            status_code=400,
            content=result
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "source": "CloudOps_AI",
                "error_type": "internal_server_error",
                "message": (
                    "Unable to approve rule candidate."
                ),
                "pattern": pattern
            }
        )

@app.post("/rules/candidates/{pattern}/reject")
def reject_rule_candidate(pattern: str):
        try:
            result = rule_approval.reject(pattern)
            if result.get("status") == "success":
                return JSONResponse(
                    status_code=200,
                    content=result
                )

            if result.get("status") == "already_rejected":
                return JSONResponse(
                    status_code=200,
                    content=result
                )

            if result.get("status") == "not_found":
                return JSONResponse(
                    status_code=404,
                    content=result
                )

            return JSONResponse(
                status_code=400,
                content=result
            )

        except Exception:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "source": "CloudOps_AI",
                    "error_type": "internal_server_error",
                    "message": (
                        "Unable to reject rule candidate."
                    ),
                    "pattern": pattern
                }
            )

@app.post("/rules/candidates/{pattern}/promote")
def promote_rule_candidate(pattern: str):
        try:
            result = rule_approval.promote(pattern)
            if result.get("status") == "success":
                return JSONResponse(
                    status_code=200,
                    content=result
                )

            if result.get("status") == "not_found":
                return JSONResponse(
                    status_code=404,
                    content=result
                )

            if result.get("status") == "duplicate":
                return JSONResponse(
                    status_code=409,
                    content=result
                )

            return JSONResponse(
                status_code=400,
                content=result
            )

        except Exception:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "source": "CloudOps_AI",
                    "error_type": "internal_server_error",
                    "message": (
                        "Unable to promote rule candidate."
                    ),
                    "pattern": pattern
                }
            )

@app.get("/rules/promoted")
def list_promoted_rules():
        try:
            promoted_rules = rule_promoter._load()
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "count": len(promoted_rules),
                    "rules": promoted_rules
                }
            )
        
        except Exception:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "source": "CloudOps_AI",
                    "error_type": "internal_server_error",
                    "message": "Unable to load promoted rules."
                }
            )
