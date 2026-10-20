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

Review PLAN.md and confirm the model/setup before collecting responses. No experiment results are included in this package.

Incomplete or malformed runs produce an INCONCLUSIVE report. Existing result folders are never overwritten.
