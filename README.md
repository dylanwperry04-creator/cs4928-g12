# CS4928 G12 / P12: Inline Comment Smell Detection and Repair

Team: Tommy Quinn, Dylan Perry, Sean Coughlan

Assigned study: Çağlar et al., "Automated Inline Comment Smell Detection and Repair with Large Language Models", ASE 2025 (https://doi.org/10.1109/ASE63991.2025.00088). Dataset from the linked Figshare package 27131295.

| Folder / file | What it is |
|---|---|
| `original_artefact/` | Figshare download, unchanged |
| `prompts/detection_prompt.txt` | The fixed detection prompt |
| `inputs/` | The 50 sampled cases and the five batches prepared for the model |
| `reference/labels.csv` | Ground-truth labels. Never sent to the model |
| `scripts/prepare_inputs.py` | Builds `inputs/` and `reference/` from the dataset |
| `PLAN.md` | Research questions, collection procedure and scoring decision rule |
| `runs/` | Raw model replies, saved unchanged, plus the run log |
| `AI_LOG.md`, `DEVIATIONS.md` | AI use and departures from the paper |
| `scripts/score.py` | Scores a saved run |
| `tests/` | Checks for the scoring maths |
| `results/` | Scored output for each run |

## Reproduce

```bash
python3 scripts/prepare_inputs.py              # rebuilds inputs/ (byte-identical)
python3 -m unittest discover tests             # scoring checks
python3 scripts/score.py runs/run_01           # scores a saved run into results/run_01
```
Python 3.10+, standard library only.

Review PLAN.md and confirm the model/setup before collecting responses. Saved M2 results are in results/run_01; the completed Event A comparison is linked below.

Incomplete or malformed runs produce an INCONCLUSIVE report. Existing result folders are never overwritten.

## Event A transfer test

[Results and interpretation](event_a/RESULTS.md) compare the frozen later-snapshot run with M2, review comment evolution, and distinguish the original score from post-run sensitivity checks.

- [Raw replies and run log](event_a/runs/run_01/)
- [Frozen first-result scores](event_a/results/run_01/metrics.json)
- [Source review](event_a/review/comment_review.csv)
- [Validation and reproduction](event_a/VALIDATION.md)
- [Text for the shared tracker](event_a/TRACKER_ENTRY.md)

Recompute the supplemental audit with `python scripts/analyse_event_a.py event_a/runs/run_01`. The frozen scorer refuses to overwrite its checked-in results.
