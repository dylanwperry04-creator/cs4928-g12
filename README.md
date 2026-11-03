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

Review PLAN.md and confirm the model/setup before collecting responses. No experiment results are included in this package.

Incomplete or malformed runs produce an INCONCLUSIVE report. Existing result folders are never overwritten.

## Week 9 design review (RQ2)

Reviewed the first ten flagged comments in `results/run_01/repair_candidates.csv` in sample order. Compared the AnkiDroid Java snapshots at `79163e4b57` (2021) and `9db834afd0` (2022) in `event_a/source/`. Line numbers below refer to those snapshots. The later labels are manual judgements under the original taxonomy. A removed comment has no later label.

| Case | 2021 line(s) → 2022 line(s) | M2 prediction → later label | Decision and code evidence |
| --- | --- | --- | --- |
| 000001 | 90 → absent | Task → — | Removed. The old `PreferenceContext` declaration and its #5019 TODO are gone. |
| 000002 | 99 → absent | Task → — | Removed. `Preferences` now extends `AnkiActivity` (line 112) and no longer carries the #5019 TODO. |
| 000004 | 108 → 120 | Beautification → Beautification | Keep. The heading still marks the start of preference fields after the public notification constant. |
| 000005 | 120–122 → 199–201 | Beautification → Beautification | Keep. The divider still marks the transition from fields to overridden methods before `onCreate`. |
| 000006 | 128 → 210 | Obvious → Obvious | Remove the comment. The two calls below already describe the action-bar setup. |
| 000010 | 210–212 → 291–293 | Beautification → Beautification | Keep. The divider still separates lifecycle overrides from the helper methods below. |
| 000011 | 236 → 890 | Obvious → Obvious | Remove the comment. `initializeLanguageDialog(screen)` already states what happens. |
| 000013 | 255 → absent | Beautification → — | Removed. The 2021 label was Obvious, so the M2 prediction was wrong then. The old comment is absent even though the 2022 code still has custom-button settings (line 1409). |
| 000014 | 305 → 1411 | Obvious → Obvious | Keep. The comment still describes the whole reset block, which clears several preference keys and refreshes the screen (lines 1412–1437). |
| 000015 | 330 → absent | Commented out code → — | Removed. The Event A matcher picked up the live `finish();` call in `closePreferences()` at line 519. The manual check in `event_a/stale_review.csv` distinguishes them. |

All six surviving comments retain their original label and agree with the M2 prediction. Four were removed upstream. Two surviving comments have a justified repair.

### Design decision

The comments in 000006 and 000011 duplicate what their adjacent method calls already communicate. Keeping them would preserve the existing text but leave two descriptions to maintain. Extracting or renaming methods would change the structure for calls that are already clear. Remove just the two redundant comments. Retain the section markers and the reset summary where they help a reader navigate the class. The patch targets the later Java snapshot and can be applied with `git apply` in an AnkiDroid checkout at `9db834afd0`.

```diff
--- a/AnkiDroid/src/main/java/com/ichi2/anki/Preferences.java
+++ b/AnkiDroid/src/main/java/com/ichi2/anki/Preferences.java
@@ -207,7 +207,6 @@
 
         enableToolbar();
 
-        // Add a home button to the actionbar
         getSupportActionBar().setHomeButtonEnabled(true);
         getSupportActionBar().setDisplayHomeAsUpEnabled(true);
         setTitle(getResources().getText(R.string.preferences_title));
@@ -887,7 +886,6 @@
                 category.removePreference(checkBoxPref_Vibrate);
                 category.removePreference(checkBoxPref_Blink);
             }
-            // Build languages
             initializeLanguageDialog(screen);
         }
 
```

### Verification

The patch passed `git apply --check` and applied cleanly to a copy of the pinned Java source. A byte comparison confirmed that the repaired file differs only by deletion of the two standalone comment lines. Reversing the patch restored the original bytes. This verifies the source-level behaviour claim. An Android build or runtime test was outside this check. The Event A inputs and results remain reproducible from the original snapshots.

