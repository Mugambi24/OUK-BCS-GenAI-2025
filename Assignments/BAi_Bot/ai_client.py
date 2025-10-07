# ai_client.py
import os
import re
import json
from typing import Optional, Any, Dict
from google import genai
from google.genai import types

# The client will pick up GEMINI_API_KEY from the environment automatically,
# or you can pass api_key=str in genai.Client(api_key="...") for testing.
client = genai.Client()

DNA_RE = re.compile(r'^[ATCGNatcgn]+$')

def validate_dna(seq: str) -> bool:
    return bool(seq) and bool(DNA_RE.match(seq))

def gc_content(seq: str) -> float:
    s = seq.upper()
    if len(s) == 0:
        return 0.0
    g = s.count("G")
    c = s.count("C")
    return round((g + c) / len(s) * 100, 2)

def _build_prompt(seq: str, organism: Optional[str] = None) -> str:
    gc = gc_content(seq)
    organism_line = f"Organism: {organism}" if organism else ""
    # Strong instruction to avoid lab protocols (safety)
    return f"""
You are an expert bioinformatics assistant. Given the DNA sequence below and the GC value already computed, produce a short JSON object (no extra commentary) with keys:
  - gc: number (percent, use the given GC value)
  - summary: 1-2 plain-English sentences about the sequence context (conceptual only)
  - features: an array of 0..4 short strings listing possible conceptual features (e.g., 'high GC region', 'could contain short ORF', 'polyA signal (eukaryotic?)') NOT lab steps
Use the GC value supplied and do NOT provide protocols, experimental steps, or anything actionable in lab. Return valid JSON only.

Sequence: {seq}
Precomputed GC: {gc}%
{organism_line}
"""
    
def analyze_sequence(seq: str, organism: Optional[str] = None, model: str = "gemini-2.5-flash") -> Dict[str, Any]:
    if not validate_dna(seq):
        raise ValueError("Invalid DNA sequence: only A,T,C,G,N allowed.")
    prompt = _build_prompt(seq, organism)
    # call Gemini via google-genai SDK (quickstart pattern)
    response = client.models.generate_content(model=model, contents=prompt)
    text = response.text.strip()
    # Try to parse JSON returned by the model
    try:
        parsed = json.loads(text)
        # Ensure 'gc' at least is set
        if "gc" not in parsed:
            parsed["gc"] = gc_content(seq)
        return parsed
    except json.JSONDecodeError:
        # If LLM didn't return JSON, return both raw text and computed GC
        return {"gc": gc_content(seq), "raw": text}

if __name__ == "__main__":
    # quick manual test:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Test DNA sequence (e.g. ATGCGTACG)")
    parser.add_argument("--organism", default=None)
    args = parser.parse_args()
    seq = args.test or "ATGCGTACG"
    out = analyze_sequence(seq, args.organism)
    print(json.dumps(out, indent=2))