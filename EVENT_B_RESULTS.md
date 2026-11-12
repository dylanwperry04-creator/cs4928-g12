# Event B: results

Prediction recorded first in `EVENT_B.md` (commit 05d51f1, 18:38 on 12 Nov), before any analysis. Pre-Event-B state is tag `PRE_EVENT_B` (commit 41a203a, Week 9 design review in `README.md`).

## Pressure tested

A public API or type referenced by the code or comments is renamed. We applied IDE-style renames to the 2022 `Preferences.java` (code tokens renamed; comments and string literals untouched, which is what an IDE rename does) in two states:

- **S0**: the 2022 file as it is
- **S1**: the Week 9 design applied (the comments for cases 000006 and 000011 deleted)

| Rename | Why this one |
|---|---|
| R1 `modSchemaNoCheck` → `modSchemaWithoutConfirmation` | Public `Collection` API, named by comment 000043 |
| R2 `onRestoreInstanceState` → `onRestoreSavedState` | Public lifecycle API, named by comment 000007 |
| R3 `getSupportActionBar` → `getSupportToolbar` | The ActionBar to Toolbar direction the 2022 code already shows (`enableToolbar()`) |

Run: `python3 scripts/simulate_event_b.py` (output in `event_b/results.json` and `event_b/states/`).

## Options considered

| Option | Main trade-off |
|---|---|
| A. No additional change; rely on code review | No cost, but review already missed a real drift in this file (below) |
| **B. Add a small automated check** (chosen) | Catches comments naming a missing identifier; needs a short glossary for project names; cannot catch drift in plain English |
| C. Turn identifier mentions into Javadoc `{@link}` references, which IDE renames update | Only works in Javadoc blocks; comments 000007 and 000043 are inline `//` comments, so it means restructuring comments that are fine as they are |
| D. Delete every comment that names an identifier | Removes drift risk but also removes "why" information (000043 explains why the exception cannot happen) |

B is the smallest response that addresses the pressure. No new class, layer or pattern was added.

## Results

| | S0 original | S1 Week 9 |
|---|---|---|
| Comments in file | 87 | 85 |
| Comments naming an identifier | 22 | 22 |
| R1: comments left naming a missing identifier | 1 (000043) | 1 (000043) |
| R2: comments left naming a missing identifier | 1 (000007) | 1 (000007) |
| R3: comment now describing the old concept in plain words | 1 ("Add a home button to the actionbar") | 0 |
| Caught by the check | R1 and R2: yes. R3: no | R1 and R2: yes |

**Real drift found before any rename.** Run on the unmodified 2022 file, the check flags one comment: it documents the config key `"estTime"`, but the code reads and writes `"estTimes"`. This drift already exists in AnkiDroid, and the comment was in a part of the file that went through code review.

**Check on the 2021 file:** 1 flag (`UncaughtExceptionHandlers`, a plural of a type name, which is a false positive).

**Verification of the check itself:** `tests/test_check_comment_refs.py` (rename leaves a comment dangling and the check reports it; names inside strings count as known; plain English is not flagged). The full suite passes: `python3 -m unittest discover tests`.

## Against our prediction

| Prediction | Outcome |
|---|---|
| Comments naming identifiers drift after a rename | Yes: 000007 and 000043 |
| Week 9 kept comments (dividers, "Reset toolbar button customizations") unaffected | Yes |
| 1–4 of the 37 surviving comments name an identifier, outside the Week 9 set | Yes: 2 (000007, 000043), neither in the Week 9 set |
| Week 9 only partly supported; needs an automated check rather than more structure | Yes, with one addition: Week 9 did prevent one drift (R3) |

## Conclusion

**The Week 9 decision is partly supported.**

- **Supported:** deleting the two Obvious comments removed the only comment that went stale under the ActionBar to Toolbar rename (R3). That kind of drift is in plain English, and no identifier check would catch it. Removing "what" comments is the only protection against it.
- **Not addressed:** Week 9 changed nothing for comments that name identifiers. The count is 22 before and after, and the two in our sample drift identically under R1 and R2.
- **Response:** keep the Week 9 decision, and add `scripts/check_comment_refs.py` as an automated check to run in CI on every change. It catches identifier drift and has already found a real case (`estTime`).

**Trade-off accepted:** the check needs a small glossary (6 project and framework names) to avoid false alarms, and it will still miss drift written in plain English. That gap is covered only by Week 9's rule of deleting comments that restate the code.

**Anti-pattern risk avoided:** we did not add structure (wrappers, annotations or a comment framework) for a problem a 90-line check covers. **Risk remaining:** comments 000007 and 000043 still duplicate a method name, but they explain *why*, so we keep them and rely on the check.

## Evidence

`EVENT_B.md`, tag `PRE_EVENT_B`, `scripts/check_comment_refs.py`, `scripts/comment_glossary.txt`, `scripts/simulate_event_b.py`, `tests/test_check_comment_refs.py`, `event_b/results.json`, `event_b/states/`.
