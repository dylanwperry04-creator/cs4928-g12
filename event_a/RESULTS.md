# Event A results

The frozen Event A run scored **28/38 correct (73.7% accuracy, MCC 0.619)** against the inherited M2 labels. Scores increased, but the result supports **partial, qualified transfer**: three of seven cases with an unchanged nearby window changed label, exceeding the pre-recorded 30% challenge. A source audit also found one active-code false match and one ambiguous duplicate identity. These findings limit a claim that the method transfers reliably to evolving comments.

## Material and frozen method

- Original snapshot: AnkiDroid `Preferences.java`, `79163e4b57` (4 May 2021).
- Held-out snapshot: the same file, `9db834afd0` (28 February 2022).
- Preparation and prediction: commits [3e4db15](https://github.com/dylanwperry04-creator/cs4928-g12/commit/3e4db15291a699e84f24caaf7e0abe91fbb30c46) and [b94bbea](https://github.com/dylanwperry04-creator/cs4928-g12/commit/b94bbea54d0c2238f531d454168fb03f3709f9e6).
- Raw collection: [b872489](https://github.com/dylanwperry04-creator/cs4928-g12/commit/b872489ab9580c83f26e7169870f6c5fe73905e5), 30 October 2026, 15:21-15:31 Europe/Dublin.
- The fixed prompt, taxonomy, 20-before/30-after context window and scoring functions were retained. The operator recorded GPT-6, High thinking and Temporary Chat.
- Four complete JSON replies contain 10, 10, 10 and 8 cases. All expected IDs, fields and label values validated.
- Original inputs, labels, raw replies, source snapshots and first-result metrics remain unchanged. Subsequent review and exclusions below are explicitly post-run analysis.

The automatic mapping reports 38 matches and 12 unmatched cases, with seven matches classified as `unchanged` and 31 as `code_changed`. These are automatic matching outcomes, not proof that every matched comment survived correctly. The source audit below qualifies those counts.

## Comparison with M2

| Comparison | Cases | Correct | Accuracy | MCC |
|---|---:|---:|---:|---:|
| M2 full original sample | 50 | 33 | 0.660 | 0.576 |
| M2 restricted to the same 38 automatic matches | 38 | 24 | 0.632 | 0.502 |
| Event A frozen first result | 38 | 28 | 0.737 | 0.619 |

Relative to the full M2 result cited in the prediction, accuracy increased by 0.077 and MCC by 0.042, both within 0.10. On the same 38 cases, the increases were 0.105 and 0.117. The latter comparison controls for the changed case set and is reported separately rather than substituted for the original prediction.

Across these 38 cases, five reference-label errors became correct and one correct answer became incorrect. Overall label agreement was 32/38 (84.2%). This is descriptive evidence of improved agreement with inherited labels, not evidence of general improvement across projects.

The frozen scorer returns **NOT REPRODUCED versus the paper** because MCC 0.618804 exceeds the pre-agreed upper limit of 0.61. Accuracy is inside its permitted range. This two-sided decision means that one score is slightly above the band; it does not mean performance deteriorated. The original M2 decision remains REPRODUCED.

See [first-result metrics](results/run_01/metrics.json), [comparison](results/run_01/comparison.csv), [per-class scores](results/run_01/per_class.csv) and [case-level predictions](results/run_01/predictions.csv).

## Pre-recorded expectations

| Expectation or challenge | Observed result | Interpretation |
|---|---|---|
| At least 40 comments survive | 38 automatic matches; one is not a comment | Survival prediction not met |
| Accuracy and MCC stay within 0.10 of full M2 | Changes +0.077 and +0.042 | Met against the full M2 values specified beforehand |
| A score drops by more than 0.10 | Neither score dropped | Performance-drop challenge not triggered |
| More than 30% of unchanged cases change label | 3/7 = 42.9% | Stability challenge triggered |
| 2-5 comments become stale/misaligned and most are missed | No newly stale comment conclusively established from the supplied sources | Not established; do not count uncertain warnings or an old defect as new staleness |

The three unchanged-window flips are `dataset:000037`, `000047` and `000049`: each moved from Beautification to Obvious and became correct against the inherited label. Thus the stability challenge is triggered even though those predictions improved.

Here, unchanged means equality of the nonblank, indentation-normalized three lines on either side of the target, including the target. **None of the seven cases had an identical full normalized 20/30-line context.** Their wider code context, batch membership and displayed line numbers changed. The flips therefore do not demonstrate inconsistency on identical model inputs or isolate code evolution as their cause. There are only seven such cases and one run per snapshot.

## Source review and staleness

All 50 original cases were inspected against the two supplied snapshots. The review is recorded in [comment_review.csv](review/comment_review.csv); the existing [changed-case review](stale_review.csv) now contains an assessment and evidence for all 31 automatically changed cases.

| Case | Evidence in the supplied snapshots | Assessment |
|---|---|---|
| 000015 | Old line 330 is `//finish();`; new line 519 is active `finish();` in `closePreferences` | False match caused by ignoring comment markers; not a surviving commented-out statement |
| 000043 / 000045 | Identical warnings occur at old lines 830 (V1) and 849 (V2); the single new warning is at 1195 in the V2 branch | Greedy matching assigns it to 000043 and leaves 000045 unmatched; comment identity is ambiguous |
| 000034 | Old 635-637 and new 376-378 both read a summary and write it into the cache, while the comment says the value comes from the cache | A genuine pre-existing misalignment, not a defect introduced by evolution |
| 000027 | New 1058-1072 uses URI-based size lookup and `ContentResolver.openInputStream` instead of the old path-based file access | The Google Drive warning may need updating, but this file alone does not prove provider support or successful execution |
| 000016 | The old screen-reload TODO is absent; new 1436-1437 refreshes the preferences screen | The later source supplies the previously requested action |
| 000007 / 000012 | Restored state still replaces the initial path; the revised listener still prevents disabling buttons without gestures | Useful intent/constraint comments remain aligned despite changed code |

Among the 36 unambiguously mapped comments, 30 have retained meaning supported by the source, one has a pre-existing contradiction and five remain uncertain. The uncertainty concerns the notification constant's external uses, database/thread behavior, localization, Drive-provider behavior and Back-event timing. The extra mapped warning at 000043 has unresolved identity. These are source-based assessments, not application runtime tests or fresh independent ground-truth annotation.

For 000034 the model predicted Misleading in both runs, contrary to the inherited Obvious label. Its explanation fits the visible data flow. This illustrates a reference-label limitation: a scored disagreement may be a defensible diagnosis. The reference label is nevertheless preserved for the frozen comparison.

## Post-run sensitivity analysis

No case was replaced and no new model reply was collected.

| Analysis using inherited labels | Cases | Event A accuracy | Event A MCC | Same paper rule |
|---|---:|---:|---:|---|
| Frozen result, all automatic matches | 38 | 0.737 | 0.619 | NOT REPRODUCED |
| Exclude the active-code false match, 000015 | 37 | 0.730 | 0.598 | REPRODUCED |
| Also exclude ambiguous identity 000043 | 36 | 0.722 | 0.588 | REPRODUCED |

The separate [sensitivity table](results/run_01/sensitivity.csv) retains M2 scores on each identical subset. The boundary decision changes when the questionable mappings are excluded, showing sensitivity to sample construction. These post-run exclusions do not replace or repair the frozen first result.

## Maintainability implication

Refactoring should preserve the relationship between a comment and the responsibility it explains. The move from a large preference-selection method to settings fragments changes locations and surrounding context; matching text alone cannot establish that the same responsibility survived. Comment-aware matching and enclosing-method checks are warranted in future evaluations.

For the concrete data-flow error at 000034, a small comment correction improves comprehensibility without changing behavior: **Cache the original summary before updating the displayed summary.** A [proposed comment-only diff](review/summary_comment_fix.diff) is supplied against the later upstream path. It was checked on a disposable copy; the recorded snapshot is untouched. No design pattern or executable refactor is justified by this evidence.

## Scope and evidence

This tests transfer across two versions of one file, not across unseen projects. Five of the ten reference classes have no examples among the 38 cases. The inherited labels were not independently re-annotated for 2022. The review was performed after seeing results with ChatGPT/Codex assistance and is not a blinded human assessment.

The uploaded Event A log records account memory off; the M2 log records it left on. Both state Temporary Chat, so the account-toggle difference alone does not establish an effective prompt difference. Custom-instruction settings are not recorded. Changed contexts/batches and one-run variation limit attribution to code evolution. The raw logs have been retained as uploaded.

The prediction was committed before collection. Its entry time in the shared tracker was not available for verification. [Tracker text](TRACKER_ENTRY.md) is prepared for the group to enter; no workbook update is claimed.

[Validation and reproduction](VALIDATION.md) lists the completed checks. [audit.json](results/run_01/audit.json) records exact scores, paired changes and challenge checks; [file_manifest.json](results/run_01/file_manifest.json) records hashes of the frozen evidence.
