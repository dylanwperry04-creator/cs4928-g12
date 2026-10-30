# Deviations from the paper

| # | Date | Deviation | Why | Effect on results |
|---|---|---|---|---|
| D1 | 20 Oct 2026 | 50 cases instead of 2,211; all from one file | Bounded task in the P12 pack | Results are not representative of the full dataset; rare classes barely present |
| D2 | 20 Oct 2026 | One current model, one run, zero-shot only (paper: 4 models, 5 runs, zero- and few-shot) | Bounded task; no API budget | No run-to-run variance estimate |
| D3 | 20 Oct 2026 | Our own prompt adapted from the supplied taxonomy (paper's exact prompts not in the package) | Paper's repair package link returned 403 | Prompt wording may affect results |
| D4 | 20 Oct 2026 | Older 2,448-comment dataset from Figshare, not the paper's cleaned 2,211 version | Only the older one is in the supplied package | Some labels may differ from the paper's |
| D5 | 20 Oct 2026 | Comments sent in batches of 10 with 20/30 lines of context | Practical limit for manual runs | Cases in a batch could influence each other |
| D6 | 21 Oct 2026 | Batches run in ChatGPT Temporary Chat with account memory left on; custom instructions setting not recorded (plan said memory and custom instructions disabled) | Operator did not want to change account settings | Temporary Chat does not use saved memory according to OpenAI; small risk that account settings influenced replies |
| D7 | 30 Oct 2026 | Event A uses inherited M2 labels for later code, without new independent ground truth | Frozen first comparison specified the same scorer and reference taxonomy | Scores measure agreement with inherited labels; the post-run source review is separate and does not relabel the first result |
| D8 | 30 Oct 2026 | Post-run audit found one active-code false match (000015) and an ambiguous repeated-comment identity (000043/000045) | Text matching removes comment markers and assigns duplicate occurrences greedily | Original mapping, inputs and 38-case first score preserved; exclusions reported only as post-run 37- and 36-case sensitivities |
| D9 | 30 Oct 2026 | Event A uploaded run log records account memory off; M2 log records it left on; custom-instruction settings are not recorded | Configuration as recorded by the operator in each saved log | Both logs state Temporary Chat; an effective prompt difference from the account toggle is not established. Custom instructions are unrecorded; full context, batching and one-run variation also limit causal claims |
