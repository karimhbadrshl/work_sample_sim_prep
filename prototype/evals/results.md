# Evaluation results (synthetic data, mode = mock, model = mock-rules, prompt = cfwc-v0.2)

## 1. Agreement with intended scores

*n* = 21 invented responses spanning 0-4.

| Statistic | Value |
|---|---|
| Quadratic weighted kappa | .92 (95% bootstrap CI .82 to .97) |
| Exact agreement | 71% |
| Adjacent agreement (within 1) | 100% |
| Standardised mean difference (machine - intended) | .07 |
| Routed to human review | 4 of 21 |

Confusion matrix (rows = intended, columns = machine):

| | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **0** | 1 | 1 | 0 | 0 | 0 |
| **1** | 1 | 3 | 0 | 0 | 0 |
| **2** | 0 | 0 | 3 | 2 | 0 |
| **3** | 0 | 0 | 1 | 3 | 1 |
| **4** | 0 | 0 | 0 | 0 | 5 |

Disagreements of 2+ points: none

## 2. Repeat-run consistency

Identical score on all 3 runs: 100% of items. Not informative in mock mode (rules are deterministic); re-run in live mode.

## 3. Robustness cases

| Case | Expected | Score | Review? | Flags |
|---|---|---|---|---|
| r_empty | review | None | yes | too_short |
| r_short | review | None | yes | too_short |
| r_gibberish | review | None | yes | too_short, gibberish |
| r_offtopic | review_or_0 | 0 | yes | off_topic |
| r_injection | review | 2 | yes | injection_attempt |
| r_keyword_stuffing | low_score | None | yes | no_sentence_structure |
| r_outside_policy | flag | 4 | yes | outside_policy |
| r_very_long | review | None | yes | too_long |

## 4. Matched pairs (content identical, one non-construct feature changed)

| Pair | Feature changed | Score A | Score B | Gap |
|---|---|---|---|---|
| f1_spelling_us_uk | US vs UK spelling | 4 | 4 | +0 |
| f2_minor_typos | Minor spelling slips | 4 | 3 | -1 |
| f3_dialect | Non-standard / regional English phrasing | 4 | 4 | +0 |
| f4_agent_name | Sign-off name | 4 | 4 | +0 |
| f5_lowercase | All-lowercase formatting | 4 | 4 | +0 |
| f6_bullets | Bulleted vs prose layout | 4 | 4 | +0 |

Mean gap (B - A) = -0.17; pairs with |gap| >= 1: 1 of 6.

## What this does not show

- No real human ratings: 'intended' scores were written by the task author, so agreement is optimistic.
- Small *n*; wide intervals. Not evidence of validity for hiring decisions.
- Matched pairs test a handful of features, not adverse impact on real demographic groups.