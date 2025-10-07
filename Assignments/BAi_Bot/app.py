# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import ai_client

app = FastAPI(title="BAi_Bot AI Genomics API")

class SequenceIn(BaseModel):
    sequence: str
    organism: Optional[str] = None

@app.post("/analyze")
def analyze(payload: SequenceIn):
    seq = payload.sequence.strip()
    if not ai_client.validate_dna(seq):
        raise HTTPException(status_code=400, detail="Invalid DNA sequence; only A,T,C,G,N allowed.")
    try:
        res = ai_client.analyze_sequence(seq, payload.organism)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True, "data": res}
