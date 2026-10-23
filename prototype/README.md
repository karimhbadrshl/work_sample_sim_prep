# Prototype: technical README

The candidate replies to an upset customer. The reply is scored 0-4 on **customer-focused written communication** against an anchored rubric with five behavioural indicators. Each score comes with quoted evidence (verified against the reply) and a human-review decision. All content is synthetic.

## Run locally (mock mode: no key, no network)

From the repo root:

```bash
python -m venv .venv
.venv/Scripts/activate            # macOS/Linux: source .venv/bin/activate
pip install -r prototype/requirements.txt
streamlit run prototype/app.py
python prototype/evals/run_eval.py   # writes prototype/evals/results.md and results.json
```

## Live mode (Anthropic API)

```bash
set LLM_MODE=live                 # PowerShell: $env:LLM_MODE="live"
set ANTHROPIC_API_KEY=...         # never in a file
set LLM_MODEL=claude-opus-5-5     # optional; this is the default
```

Live calls use structured outputs (the JSON schema is in `config.py`), low effort, one retry and server-side refusal fallback. Output is validated locally, and every quote must appear in the reply. Current Claude models don't accept `temperature`, so repeat-run consistency has to be measured.

## Static browser build (the public demo)

`python tools/build_static.py` writes `docs/index.html`. It embeds these files and runs them in the browser with [stlite](https://github.com/whitphx/stlite) v1.9.2 (Streamlit on Pyodide), always in mock mode. GitHub Pages serves it from `/docs`, and the file also works when opened directly (online). Re-run it after any change here.

## Files

| File | What it is |
|---|---|
| `config.py` | Stimulus, policy notes, indicators, rubric, system prompt, output schema, version label, app title |
| `scorer.py` | Pre-checks, then mock or live scorer, then validation, then review routing |
| `app.py` | UI: candidate view and recruiter view, audit record; tabs for evidence and approach |
| `brand.py` | Visual identity (fonts, colours, brick mark); theme colours in `../.streamlit/config.toml` |
| `APPROACH.md` | One-screen summary shown in the app |
| `data/` | 21 invented replies with intended scores; robustness cases and matched pairs |
| `evals/` | Evaluation script and results (`results_v0.1.md` is the run that prompted the v0.2 guard) |

## Known limits

- The live mode follows the current SDK documentation but wasn't scored end to end, because there was no key. All reported numbers are mock-mode numbers.
- Small synthetic gold set; the rubric author also wrote the intended scores.
- No persistence, authentication or accessibility testing yet.
