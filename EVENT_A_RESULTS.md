# Event A: results

Prediction and held-out snapshot recorded first in `EVENT_A.md` (commit 3e4db15, 13:29 on 30 Oct), before inputs were built or the model was run.

## What we did

- Held-out snapshot: AnkiDroid `Preferences.java` at commit `9db834afd0` (28 Feb 2022), the last Java version. M2 used commit `79163e4b57` (4 May 2021), identified by matching the dataset's source hash. 44 commits and 10 months of evolution between them.
- `scripts/prepare_event_a.py` located each of the 50 M2 comments in the later file and rebuilt the inputs with the unchanged M2 prompt and 20/30-line context window (`event_a/mapping.csv`, `event_a/inputs/`).
- Run by Tommy: GPT-6, High thinking, ChatGPT Temporary Chat, 4 batches (`event_a/runs/run_01/`).
- Scored with `scripts/score_event_a.py`, which reuses the M2 scoring functions unchanged (`event_a/results/run_01/`).
- Each surviving comment whose nearby code changed was reviewed by hand against the 2021 and 2022 code (`event_a/stale_review.csv`). The review sheet was prepared before the scores were viewed; it was committed a minute after scoring because the file had not finished downloading.

## Results

**Survival.** 37 of 50 comments still exist in 2022; 13 were deleted (26%). The script reported 38, but the review found one false match (case 015, see D7): the commented-out `//finish();` was deleted and the script matched a live `finish();` call elsewhere. The model itself flagged this case as having insufficient context.

| Removed comments | Count |
|---|---|
| Task | 4 of 7 (two were "TODO tracked in #5019: convert to fragments", and that conversion was completed) |
| Obvious | 4 |
| Not a smell | 3 |
| Vague | 1 |
| Commented out code | 1 (case 015) |

**Staleness.** Of the 37 surviving comments, 30 had code changed right next to them (mostly the migration from `android.preference` to androidx). All 30 were judged still accurate. No surviving comment had become stale or misleading.

**Detection on the later snapshot** (37 genuine survivors, case 015 excluded; 38 in brackets):

| | Accuracy | MCC |
|---|---|---|
| Event A, 2022 code | 0.730 (0.737) | 0.598 (0.619) |
| M2, same comments in 2021 code | 0.622 (0.632) | 0.477 (0.502) |
| M2, all 50 | 0.660 | 0.576 |

**Label stability.** The model gave a different label from M2 for 6 of 38 comments (84% agreement). Four were Obvious comments that M2 labelled Beautification and Event A labelled correctly as Obvious; three of these had identical nearby code. One Task changed from Not a smell to Task (now correct), and one Obvious changed to Not a smell (now wrong).

## Against our prediction

| Prediction | Outcome |
|---|---|
| 40+ comments survive | No: 37 |
| Accuracy and MCC on survivors within ±0.10 of M2 (0.66 / 0.58) | Yes: 0.73 / 0.60 |
| 2–5 comments become stale; model misses most | No: 0 stale among survivors, so the second part could not be tested |
| Challenge: accuracy or MCC drop by more than 0.10 | Did not happen; both rose |
| Challenge: model changes label on more than 30% of unchanged comments | **Met**: 3 of 7 (43%), though on a very small subset |

Applying the frozen paper rule to Event A gives NOT REPRODUCED, only because MCC 0.619 exceeds the upper bound of 0.61 by 0.009. The model did better, not worse. Excluding case 015, MCC is 0.598 and the rule gives REPRODUCED.

## What transfers and what does not

- **Transfers:** overall detection performance. On later code the model scored at least as well as in M2, and the M2 REPRODUCED conclusion is not weakened.
- **Label changes:** Cases 037, 047 and 049 changed from Beautification in M2 to Obvious in Event A even though the three lines on either side were unchanged. The wider code context and batch contents differed, so the comparison cannot establish what caused the label changes.
- **Evolution effect:** in this file, evolution removed comments rather than making them stale. Comments disappeared with the code or task they described; surviving comments were carried through refactors and stayed accurate.

## Design / maintainability implication

18 of the 37 survivors are Obvious comments that restate the next line of code. They stayed accurate, but every API migration touched the code right beside them, so each one was something a developer had to read and check during 44 commits of refactoring without it adding information. This supports the refactoring guideline that a comment explaining *what* code does is a sign the code should explain itself: renaming, or Extract Method, so the method name carries the meaning (for example, a block under `// Make it possible to test crash reporting, but only for DEBUG builds` becomes `addDebugCrashTestPreference()`). Comments explaining *why* (workarounds such as #5864, the PERF note, the snackbar space note) carried information the code cannot, and should stay. Task comments linked to an issue number (#5019) were removed when the work was done, which suggests linking TODOs to issues keeps them from going stale. No design pattern is justified by this evidence.

## Evidence

`EVENT_A.md`, `event_a/mapping.csv`, `event_a/stale_review.csv`, `event_a/runs/run_01/`, `event_a/results/run_01/metrics.json`, `predictions.csv`, `per_class.csv`, `scripts/prepare_event_a.py`, `scripts/score_event_a.py`.
