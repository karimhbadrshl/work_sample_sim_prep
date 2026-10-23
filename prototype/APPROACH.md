## The approach in brief

**The problem.** The client's multiple-choice screen doesn't tell hiring managers whether entry-level contact-centre agents can write to an upset customer. This prototype tests a short written task instead, scored by AI with evidence a recruiter can check.

**How a reply is scored**

1. **Rule checks first, no AI.** Replies that are empty, too short, too long, gibberish, a list of words or an obvious attempt to manipulate the scorer get no automated score. A person looks at them.
2. **AI rating against a rubric.** The model rates the reply 0-4 against an anchored rubric with five observable indicators: acknowledges the problem, takes ownership, offers a concrete resolution, gives clear next steps, and keeps a professional tone. It returns structured data, not free text.
3. **Every claim is checked.** Each indicator has to be backed by an exact quote from the reply. If a quote can't be found in the reply, the reply goes to a person.
4. **People stay in the loop.** Any flag, or confidence below .6, means a person reviews before a decision.

**Key decisions**

- I chose one holistic score with indicator evidence over five sub-scores. Five sub-scores from 150 words would be noisy.
- Spelling and regional English are explicitly *not* scored. The construct is customer focus, not standard-English correctness.
- No AI-text or emotion detection. Detectors are unreliable and biased, and emotion inference at work is prohibited in the EU.

**What the evidence shows, and what it doesn't.** See *Evidence*. These results come from synthetic data in mock mode. They test the pipeline and its safeguards, not the AI model's accuracy. Real evidence needs double-rated real replies, a pilot, and validation against job performance.

*The full write-up, with the psychometric reasoning, is submitted separately as a Word document.*
