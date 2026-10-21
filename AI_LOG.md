# AI use log

Only AI use that changed a decision or result.

| # | Date | Tool | What it did | How we checked it | Outcome |
|---|---|---|---|---|---|
| A1 | 17 to 19 Oct 2026 | ChatGPT / Codex | Generated the 50-case sample rule, batches, prompt and a first scorer | Read through it; the sample rule and batches were correct, but most of the code and supporting documents were far more than the task needed | Kept the sample rule, batches and prompt; dropped the rest as over-engineered |
| A2 | 20 Oct 2026 | Claude | Rewrote the input builder and scorer in about 200 lines | `prepare_inputs.py` produces byte-identical batches to the first version; scorer accuracy/MCC match scikit-learn on a test run; unit tests in `tests/` | Accepted. Tommy then added stricter input validation and boundary tests (`tests/test_score_validation.py`) |
| A3 | 20 Oct 2026 | Claude | Suggested the ±0.10 tolerance against the paper's o3-mini zero-shot results | Checked the paper's Table IV values ourselves; tolerance based on the standard error for 50 cases | Accepted before running |
