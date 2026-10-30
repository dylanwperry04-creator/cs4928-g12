# Event A tracker entry

For G12 / P12. These are the four Event A fields to paste into the shared student tracker. The repository contains the supporting detail.

## Held out material and evidence reference

AnkiDroid Preferences.java at 9db834afd0 (28 February 2022), compared with M2 snapshot 79163e4b57 (4 May 2021). The 50 M2 IDs were mapped by comment text: 38 automatic matches in four batches (10/10/10/8), 12 unmatched. Post-run review identifies one active-code false match and one ambiguous duplicate identity among those matches. Prompt, taxonomy, context-window size and scorer were kept fixed.

Pre-run plan: https://github.com/dylanwperry04-creator/cs4928-g12/blob/3e4db15291a699e84f24caaf7e0abe91fbb30c46/EVENT_A.md

## Prediction before execution

The pre-run repository prediction was: 40+ comments survive; surviving-comment accuracy and MCC remain within 0.10 of full M2 (0.66 / approximately 0.58); 2-5 comments become stale/misaligned and most are missed. A score drop over 0.10 or label changes in more than 30% of unchanged cases would challenge the M2 conclusion.

This prediction is evidenced by the pre-run commit above. Keep an existing pre-run tracker entry intact. If it was not entered before execution, record this as a later entry linking to the earlier commit; do not backdate it.

## Event A result and decision

Partial, qualified transfer. Frozen result: 28/38 correct, accuracy 0.737, MCC 0.619, versus full M2 0.660/0.576. On the same 38 cases M2 was 0.632/0.502. Scores increased, but 3/7 unchanged nearby-window cases changed label (42.9%), triggering the pre-recorded stability challenge. Their full model contexts changed. The paper-band decision is NOT REPRODUCED solely because MCC exceeds the upper bound of 0.61. A false active-code match and ambiguous duplicate limit interpretation. Separate post-run sensitivities give 0.730/0.598 (37 cases) and 0.722/0.588 (36); neither replaces the frozen result. No newly stale case was conclusively established; one misleading cache comment was already wrong in M2. Maintainability implication: review comment-to-code identity during refactoring and prefer a small evidence-based comment fix over an unjustified design pattern.

## Supporting evidence link

Main analysis:
https://github.com/dylanwperry04-creator/cs4928-g12/blob/main/event_a/RESULTS.md

Raw collection commit:
https://github.com/dylanwperry04-creator/cs4928-g12/commit/b872489ab9580c83f26e7169870f6c5fe73905e5

Frozen scores:
https://github.com/dylanwperry04-creator/cs4928-g12/blob/main/event_a/results/run_01/metrics.json

Validation and exact reproduction commands:
https://github.com/dylanwperry04-creator/cs4928-g12/blob/main/event_a/VALIDATION.md
