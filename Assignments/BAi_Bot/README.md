# BAi_Bot — AI-Enhanced Genomics Predictor

A small, educational project that demonstrates how to combine Jac (scale-agnostic, cloud-ready language) with an LLM-backed AI layer (Google Gemini) to produce contextual, human-friendly interpretations of short DNA sequences.

## What this repo contains

* `predictor.jac` — a Jac walker that accepts short DNA sequences and returns an AI-augmented interpretation.
* `ai_client.py` — a tiny Python helper that calls the Gemini API (server-side) and returns model text.
* `config.json` / `.env.example` — where you put your `GEMINI_API_KEY` (do **not** commit secrets).
* `.gitignore` — keeps virtualenvs and secrets out of the repo.

## Key ideas

1. **Scale-agnostic design (Jac):** write once and run locally or `jac serve` to expose the walkers as HTTP endpoints.
2. **AI integration (byLLM / Gemini):** the heavy-lifting LLM is called from a server-side Python helper; responses are used as intelligent hints about the sequence (GC-content, likely features, suggested experiments *at a conceptual level* — no lab protocols).

## Quick setup (developer machine)

1. Clone the repo:

```bash
# on your machine
git clone https://github.com/Mugambi24/BAI_BOT.git
cd BAI_BOT
```

2. Create & activate a virtualenv (recommended):

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -U jaclang jac-cloud byllm google-genai
```

4. Copy example env and add your Gemini key (server-side):

```bash
cp .env.example .env
# edit .env and set GEMINI_API_KEY=your_real_key
```

5. Run locally (quick smoke-test):

```bash
# run python helper to sanity-check the Gemini call
python ai_client.py --test "ATGCGTACG"

# run jac in local test mode (syntax/example)
jac run predictor.jac --Predictor.predict_feature "ATGCGTACG" "Organism Example"
```

6. Serve as an HTTP API:

```bash
# jac-cloud will expose walkers automatically
jac serve predictor.jac
# then test with curl (example)
curl -X POST http://localhost:8080/predict_feature \
  -H "Content-Type: application/json" \
  -d '{"sequence": "CCGGATTCC", "organism": "Deep-sea Bacterium"}'
```

## Security notes

* **Never commit** your `GEMINI_API_KEY` or `.env` to GitHub. Add `.env` to `.gitignore` (the repo already contains `.gitignore`).
* Make LLM requests from server-side code only; do not embed keys in frontend code or client-side bundles.

## How to update the README on GitHub (from VS Code)

1. Open the repository in VS Code (`code .`).
2. Edit `README.md` or replace it with your improved file.
3. Use the Source Control panel to stage and commit changes, then click **Publish** / **Push** to send them to GitHub. (You may need to sign into GitHub inside VS Code.)

