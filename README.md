# CS4928 G12 / P12: Inline Comment Smell Detection and Repair

Team: Tommy Quinn, Dylan Perry, Sean Coughlan

Assigned study: Çağlar et al., "Automated Inline Comment Smell Detection and Repair with Large Language Models", ASE 2025 (https://doi.org/10.1109/ASE63991.2025.00088). Dataset from the linked Figshare package 27131295.

| Folder / file | What it is |
|---|---|
| `original_artefact/` | Figshare download, unchanged |
| `prompts/detection_prompt.txt` | The fixed detection prompt |
| `inputs/` | The 50 sampled cases and the five batches sent to the model |
| `reference/labels.csv` | Ground-truth labels. Never sent to the model |
| `scripts/prepare_inputs.py` | Builds `inputs/` and `reference/` from the dataset |

## Rebuild the inputs

```bash
python3 scripts/prepare_inputs.py    # rebuilds inputs/ and reference/ (byte-identical)
```
Python 3.10+, standard library only.
