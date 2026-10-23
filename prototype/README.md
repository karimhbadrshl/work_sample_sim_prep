# Customer reply task: AI-scored written response (prototype)

The candidate reads an angry customer email and writes a reply of 80 to 200 words. The reply is scored 0-4 on **customer-focused written communication** against an anchored rubric with five behavioural indicators. Each score comes with a rationale, quotes from the reply as evidence, and a decision on whether a person needs to review it.

All content is synthetic. There is no real candidate data and no SHL material.

## Run it (mock mode: no key, no network)

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; use: source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
streamlit run app.py          # opens the candidate + recruiter view
python evals/run_eval.py      # writes evals/results.md
```

Mock mode is the default. Scoring uses transparent keyword rules (`mock_score` in `scorer.py`), so a reviewer can always run the app. These rules are **not** the proposed scorer. They are a deterministic baseline, and they also show why keyword approaches are not enough.

## Live mode (Anthropic API)

```bash
set LLM_MODE=live                 # PowerShell: $env:LLM_MODE="live"
set ANTHROPIC_API_KEY=...         # never put the key in a file
set LLM_MODEL=claude-opus-5-5     # optional; this is the default
```

Live calls use structured outputs: a JSON schema in `config.py`. They also use low effort, one retry, and server-side refusal fallback. The output is validated locally, and every quoted piece of evidence must appear in the reply. Note that `temperature` is no longer accepted by current Claude models, so repeat-run consistency has to be measured rather than assumed.

## Files

| File | What it is |
|---|---|
| `config.py` | Stimulus, policy notes, indicators, rubric, system prompt, output schema, version label. Everything a content expert would edit is here. |
| `scorer.py` | Pre-checks, then mock or live scorer, then validation, then the review-routing decision |
| `app.py` | Streamlit UI: candidate view and recruiter view, with the audit record |
| `data/gold_set.json` | 21 invented replies with intended scores (stand-ins for expert ratings) |
| `data/robustness_and_fairness.json` | 8 robustness cases and 6 matched pairs |
| `evals/run_eval.py` | Agreement (QWK, exact, adjacent, SMD, bootstrap CI), repeat runs, robustness, matched pairs |
| `evals/results.md`, `results_v0.1.md` | Current results and the earlier run that prompted the v0.2 guard |
| `../WRITEUP.md`, `../DECISIONS.md` | Approach write-up and decisions log |

## Known limits

- The live mode was written against the current SDK documentation but **not scored end to end**, because there was no key in this session. With a dummy key the request passes the SDK's checks and reaches the API (401), so the request shape is accepted client-side. The server's handling of the schema is untested. All reported numbers are mock-mode numbers.
- On Windows, installing into a very deep folder path can break the `anthropic` package (path-length limit). Use a short path.
- The gold set is small, and the person who wrote the rubric also wrote the intended scores.
- The prototype has no persistence or authentication, and it has no candidate-facing accommodation options yet.
