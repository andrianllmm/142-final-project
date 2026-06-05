import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from astra_core import CodeUnit, analyze_code_similarity

load_dotenv()

app = FastAPI(title="ASTRA API")

web_url = os.environ["WEB_URL"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[web_url],
    allow_methods=["POST"],
    allow_headers=["Content-Type", "ngrok-skip-browser-warning"],
)

class CodeUnitRequest(BaseModel):
    id: str
    content: str


class AnalyzeRequest(BaseModel):
    units: List[CodeUnitRequest]
    threshold: float = 0.8


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    units = [CodeUnit(id=u.id, content=u.content) for u in req.units]

    result = analyze_code_similarity(
        units=units,
        threshold=req.threshold,
    )

    return result
