"""Streamlit front end: candidate view (task + reply) and recruiter view (score, evidence, review routing).
Extra tabs show the evaluation results and the write-up, so a hosted copy is self-contained.

Run:  streamlit run app.py      (LLM_MODE=mock by default; set LLM_MODE=live and ANTHROPIC_API_KEY for the real model)
"""
import json
import pathlib
import sys

import streamlit as st

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))   # so config/scorer import the same way locally and in the browser build

import config as C  # noqa: E402
import scorer  # noqa: E402

IN_BROWSER = sys.platform == "emscripten"   # True in the static HTML build (Pyodide)

st.set_page_config(page_title="Customer reply task (prototype)", layout="wide")
st.title("Customer reply task: prototype")
st.caption(f"Mode: **{scorer.MODE}** · scorer: {scorer.MODEL if scorer.MODE == 'live' else 'mock rules (no API call)'} · "
           f"version {C.PROMPT_VERSION} · synthetic content only")

if scorer.MODE == "mock":
    st.info(
        "**How to use this demo.** 1) Pick a synthetic example from the drop-down on the left, or write your own reply. "
        "2) Press **Submit**. 3) The right-hand side shows what a recruiter would see: the score, the evidence for it, "
        "and whether a person needs to review it.  \n"
        "This hosted copy runs in **mock mode**: a simple, transparent rules scorer stands in for the AI model so the demo "
        "is free and needs no API key. The proposed AI scorer is in the code and described in the write-up."
        + ("  \nIt runs entirely in your browser: nothing you type is sent anywhere." if IN_BROWSER else "")
    )

tab_try, tab_eval, tab_write = st.tabs(["Try the task", "Evaluation results", "Write-up"])

with tab_try:
    left, right = st.columns(2)

    with left:
        st.subheader("Candidate view")
        st.markdown("**Customer email**")
        # Quote block wraps long lines; escape a leading "-" so the sign-off isn't drawn as a bullet.
        st.markdown("\n".join("> " + line.replace("- ", "\\- ", 1) if line.startswith("- ") else "> " + line
                              for line in C.CUSTOMER_EMAIL.splitlines()))
        st.markdown(C.POLICY_NOTES.replace("\n", "  \n"))
        st.markdown(f"**{C.CANDIDATE_INSTRUCTIONS}**")

        gold = json.loads((HERE / "data/gold_set.json").read_text(encoding="utf-8"))
        rf = json.loads((HERE / "data/robustness_and_fairness.json").read_text(encoding="utf-8"))
        examples = {"(write your own)": ""}
        examples |= {f"{g['id']}: intended score {g['intended']}": g["text"] for g in gold}
        examples |= {f"{c['id']}: robustness test": c["text"] for c in rf["robustness"] if "LONG_FILLER" not in c["text"]}
        pick = st.selectbox("Load a synthetic example", list(examples))
        text = st.text_area("Your reply", value=examples[pick], height=260)
        st.caption(f"{len(text.split())} words")
        go = st.button("Submit", type="primary")

    with right:
        st.subheader("Recruiter view")
        if go:
            r = scorer.score_response(text)
            if r["score"] is None:
                st.warning("Not scored automatically. Sent to a trained reviewer.")
            else:
                st.metric("Score (0-4)", r["score"], help="Holistic rubric score; see indicators below")
            if r["needs_review"]:
                st.error("Human review required: " + (", ".join(r["flags"]) or f"confidence {r['confidence']:.2f} below {C.REVIEW_CONFIDENCE}"))
            else:
                st.success(f"No review flag (confidence {r['confidence']:.2f})")
            st.markdown(f"**Rationale:** {r['rationale']}")
            if r["indicators"]:
                st.markdown("**Indicators and evidence from the reply**")
                for k, desc in C.INDICATORS.items():
                    v = r["indicators"][k]
                    mark = "✅" if v["present"] else "❌"
                    ev = f" — “{v['evidence']}”" if v["evidence"] else ""
                    st.markdown(f"{mark} **{k}**: {desc}{ev}")
            with st.expander("Audit record (what would be logged)"):
                st.json(r)
        else:
            st.info("Submit a reply to see the score, evidence and review routing.")

    with st.expander("Scoring rubric"):
        st.text(C.RUBRIC)

with tab_eval:
    st.markdown((HERE / "evals/results.md").read_text(encoding="utf-8"))

with tab_write:
    st.markdown((HERE.parent / "WRITEUP.md").read_text(encoding="utf-8"))

st.divider()
st.caption("Scores support, and do not replace, a recruiter's decision. Flagged or low-confidence replies always go to a person.")
