# AI-scored customer reply task: work-sample prototype

## ▶ [Open the live prototype](https://REPLACE-ME.streamlit.app)

You don't need to install anything. The link opens the working prototype in your browser. If you see a message that the app is asleep, click **"Yes, get this app back up!"** and wait about 30 seconds.

**Inside the prototype:**

1. **Try the task.** Pick a synthetic example reply from the drop-down, or type your own, and press **Submit**. You'll see what a recruiter would see: the score (0-4), the evidence quoted from the reply, and whether a person needs to review it. The examples labelled *robustness test* show how the system handles cheating attempts and unusable replies.
2. **Evaluation results.** Agreement with intended scores, robustness checks and matched-pair fairness checks.
3. **Write-up.** My approach, key decisions, fairness and regulatory considerations, and the path to production.

The hosted demo runs in **mock mode**. A simple, transparent rules scorer stands in for the AI model, so the demo is free and needs no API key. The AI scorer (Anthropic API, structured outputs) is in the code and switches on with one setting.

## Documents

| Document | What it covers |
|---|---|
| [WRITEUP.md](WRITEUP.md) | Approach, decisions, quality evidence, fairness, limits, path to production (two pages) |
| [DECISIONS.md](DECISIONS.md) | Decisions log: what I chose, what I rejected, and the trade-off |
| [prototype/evals/results.md](prototype/evals/results.md) | Full evaluation output |
| [BRIEF.md](BRIEF.md) | The brief this responds to |

## For technical reviewers

The code is in [prototype/](prototype/). See [prototype/README.md](prototype/README.md) for how to run it locally in mock or live mode. All data is synthetic. There is no real candidate data.
