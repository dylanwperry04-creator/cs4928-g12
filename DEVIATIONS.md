# Deviations from the paper

| # | Date | Deviation | Why | Effect on results |
|---|---|---|---|---|
| D1 | 20 Oct 2026 | 50 cases instead of 2,211; all from one file | Bounded task in the P12 pack | Results are not representative of the full dataset; rare classes barely present |
| D2 | 20 Oct 2026 | One current model, one run, zero-shot only (paper: 4 models, 5 runs, zero- and few-shot) | Bounded task; no API budget | No run-to-run variance estimate |
| D3 | 20 Oct 2026 | Our own prompt adapted from the supplied taxonomy (paper's exact prompts not in the package) | Paper's repair package link returned 403 | Prompt wording may affect results |
| D4 | 20 Oct 2026 | Older 2,448-comment dataset from Figshare, not the paper's cleaned 2,211 version | Only the older one is in the supplied package | Some labels may differ from the paper's |
| D5 | 20 Oct 2026 | Comments sent in batches of 10 with 20/30 lines of context | Practical limit for manual runs | Cases in a batch could influence each other |
| D6 | 21 Oct 2026 | Batches run in ChatGPT Temporary Chat with account memory left on; custom instructions setting not recorded (plan said memory and custom instructions disabled) | Operator did not want to change account settings | Temporary Chat does not use saved memory according to OpenAI; small risk that account settings influenced replies |
