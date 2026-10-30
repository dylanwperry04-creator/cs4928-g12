# Event A validation

Analysis date: 30 October 2026. Collection commit: `b872489ab9580c83f26e7169870f6c5fe73905e5`.

## Completed checks

| Check | Result |
|---|---|
| Existing scoring unit and validation tests | 8 tests passed |
| Rebuild original M2 sample and inputs | Byte-identical to collection commit |
| Rebuild Event A mapping, reference labels and batches | Byte-identical to collection commit |
| Saved replies and fixed prompt | Correct filenames, expected per-batch IDs/order, exact fields, valid labels/booleans and nonempty reasons |
| Frozen Event A scorer | Completed with no invalid predictions; 28/38 correct, MCC 0.618804 |
| Supplemental recomputation | Agrees with frozen metrics; includes same-case comparison and paired label changes |
| Raw responses, frozen prompts/labels/mapping, snapshots and original scorers | 35 frozen files compared byte-for-byte with the collection commit; SHA-256 values recorded in the file manifest |
| Supplemental outputs reproduced | All 8 result files reproduced byte-for-byte |
| All original cases reviewed | 50 source-review rows; 31 completed changed-case rows |
| Proposed comment-only diff | Applies to a disposable copy of the selected later source; executable content unchanged |
| Android build or device/provider tests | Not run; the full Android application is not present |
| Shared tracker update | Not performed; paste-ready text supplied separately |

## Reproduce

Python 3.10+ and the standard library are sufficient. Run from a clean checkout of the raw collection commit to reproduce the first scorer output:

```bash
python -m unittest discover tests
python scripts/prepare_inputs.py
python scripts/prepare_event_a.py
python scripts/score_event_a.py event_a/runs/run_01
```

The frozen scorer deliberately refuses to overwrite an existing results folder. In the completed analysis checkout, the checked-in first-result files already exist, so do not run that command over them.

Recompute the supplemental audit and sensitivity tables in the completed checkout with:

```bash
python scripts/analyse_event_a.py event_a/runs/run_01
```

This validates the raw replies and fixed prompt, recomputes the scores, checks them against the preserved first result, and writes the supplemental audit, comparison, sensitivity, confusion matrix and frozen-evidence hash manifest. Its source-review inputs are the explicitly post-run, AI-assisted assessments in `event_a/review/comment_review.csv`; these are not new reference labels.

The preparation commands were run before completing `event_a/stale_review.csv`. They do not write that review file or the raw replies. The original scoring code and reference labels were not modified.

## Proposed comment correction

`event_a/review/summary_comment_fix.diff` is a proposal against upstream `AnkiDroid/src/main/java/com/ichi2/anki/Preferences.java` at the selected 2022 version. It is not a modification of the recorded source snapshot or a tested Android application fix. Only the misleading cache-direction comment changes.
