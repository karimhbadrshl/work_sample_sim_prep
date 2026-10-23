# AI-scored customer reply task: approach

*Karim Badr. Work-sample prototype, synthetic data only.*

## What I built and the claim

The client wants to know whether entry-level agents can actually write to an upset customer, which their multiple-choice screen doesn't tell them. I built a short written task: the candidate replies to an angry email about a late, wrong-size birthday present. The reply is scored 0-4 on *customer-focused written communication*. Each score comes with a plain-English rationale, quotes from the reply as evidence, and a flag saying whether a person must review it.

The prototype shows the full pipeline from candidate reply to an explainable, auditable score with human-review routing. It also includes an evaluation harness that would tell us whether to trust the scores. It does **not** yet show that the scores are valid. That needs real candidates and trained human raters.

## How it works

1. **Task.** The candidate gets the customer email, three policy options (express exchange, refund, $10 voucher) and a 80-200 word guide. The policy notes make "resolution" observable and fair: everyone has the same options.
2. **Pre-checks**, with no AI involved. Empty, too short, too long, gibberish, word lists with no sentences, and obvious injection text are never auto-scored. They go to a person.
3. **Scoring.** An LLM rates the reply against an anchored rubric with five indicators: acknowledges the problem, takes ownership, offers a concrete resolution, gives clear next steps, and keeps a professional tone. It returns schema-checked JSON: whether each indicator is present, an exact quote as evidence, a 0-4 score, a rationale, confidence and flags.
4. **Validation.** Every quote is checked against the reply, and any invented quote goes to a person.
5. **Routing.** Any flag, or confidence below .6, means a person reviews before any decision.
6. **Recruiter view.** It shows the score, the evidence per indicator and the review status, plus the full audit record (model, prompt version, flags).

## Key decisions and what I rejected

- **One holistic score with indicator evidence, rather than five sub-scores.** Five sub-scores from 150 words would be noisy. The indicators give the explanation without claiming that each one can be measured separately.
- **Verifiable quotes, rather than a free-text rationale.** A rationale can sound right and still be invented. A quote can be checked by code.
- **Rules before AI for the unscorable cases.** These checks are cheap and predictable, and no number is ever produced for a non-attempt.
- **No AI-text detection in the score.** Current detectors are unreliable and tend to flag non-native writers. Integrity comes from the task design and a follow-up interview instead (see below).

## How I would judge quality

The evidence below comes from **mock mode** on **synthetic data**: a transparent keyword-rules scorer that stands in for the LLM so the app runs without a key. It tests the harness, not the LLM. On 21 invented replies with intended scores, the rules baseline reached QWK = .92 (95% bootstrap CI [.82, .97]), 71% exact and 100% adjacent agreement, SMD = .07. Four of 21 replies were routed to review. That is optimistic, because I wrote both the rubric and the intended scores.

The robustness suite did what it is for. In v0.1, a pure list of keywords scored **4 with no flag**. I added a sentence-structure guard (v0.2), after which it is routed to a person, and I report both runs. The injection attempt and the off-policy offer ("50% off") were both flagged. The matched pairs showed **one gap**: a reply with minor typos scored 3 against 4 for the clean version, because the keyword rules missed "sory". The rubric tells the LLM to ignore such slips, but that is a claim I would test, not assume.

Before any live use I would run the following:

- **Reliability.** Repeat-run agreement of the LLM (sampling can no longer be fixed with temperature, so it has to be measured), and agreement between two trained human raters as the ceiling.
- **Accuracy.** Agreement with expert ratings on about 300-500 real, double-rated replies, set against the human-human agreement. As a working standard I would want QWK ≥ .70 and within .10 of human-human, with no subgroup degradation, alongside the usual automated-scoring guidance.
- **Validity.** Content evidence from job analysis and SME review of the rubric; relations to supervisor ratings or QA scores after hire; and checks that the score is not driven by length or by style unrelated to the construct.

## Fairness and defensibility

At the design stage, the rubric excludes spelling and regional English, every candidate gets the same policy options, the scorer cannot see any demographic data or names, and no emotion or personality inference is made. I checked six matched pairs (spelling variant, typos, dialect, name, formatting); one showed a gap, as reported above.

For live use, the following apply:

- **US.** Title VII and the **Uniform Guidelines**: monitor adverse impact (four-fifths rule plus significance tests) and document validity evidence for the cut score. **SIOP Principles** for validation. **NYC Local Law 144**: an annual independent bias audit with published results, and candidate notice at least 10 business days before use. ADA: offer accommodations such as extra time or assistive technology.
- **EU.** Recruitment AI is **high-risk under the EU AI Act** (Annex III). Following the Digital Omnibus (Reg. 2026/1744), those obligations now apply from **2 December 2027**. That date gives a build window, not an exemption. The obligations cover risk management, data governance, technical documentation, logging, transparency to deployers and human oversight. GDPR Article 22 also applies because this is significant automated decision-making. The audit record and review routing in the prototype are the start of that.

## Candidate experience and integrity

The task is short (about 10 minutes) and realistic, which helps candidates see it as fair and gives them a preview of the job. The trade-off is that a free-text task is easy to complete with a chatbot. My mitigations are a timed, proctored delivery with paste detection and the policy details specific to this task. Most importantly, the score is used to *shortlist*, not to hire: the interview includes a live version of the same skill. I would not use AI-text detection to penalise anyone.

## Limits and risks

- The live LLM path follows current documentation but was **not run in this session**, and all numbers are mock-mode numbers.
- The data is synthetic, *n* = 21, and the rubric author also produced the intended scores.
- The scorer may reward polished generic apologies, or pick up a length or style bias I haven't tested.
- The model can change underneath us. Pin the model version and re-run the evaluation on every change.
- The pre-check thresholds are guesses. A review rate that is too high would cost recruiters more time than it saves.

## Path to production

- **Product and the client.** Job analysis, defining the cut score, and the recruiter workflow for reviewed cases.
- **Psychometrics.** A rater training and double-rating study, a pilot of about 500 candidates, then validation against job performance and adverse impact monitoring.
- **Engineering.** A pinned model, logging and retention, monitoring of drift and review rate, accessibility, and load testing at 40,000 candidates a year.
- **Legal and Privacy.** The LL144 audit, EU AI Act technical documentation and a DPIA, candidate notices, and accommodations.

With another week I would run the live scorer on a few hundred varied synthetic and pilot replies, compare it with two human raters, and probe length and dialect effects systematically.
