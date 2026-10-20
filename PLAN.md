# G12 / P12 — Experiment Plan

Team: Tommy Quinn, Dylan Perry, Sean Coughlan  
Plan agreed: 20 October 2026  
Status: Experiment not yet run.

## Study

Çağlar et al., “Automated Inline Comment Smell Detection and Repair
with Large Language Models”, ASE 2025.

Paper: https://doi.org/10.1109/ASE63991.2025.00088
Dataset: https://figshare.com/articles/conference_contribution/27131295

The supplied dataset is kept in original_artefact/.

## Research questions

RQ1: How accurately does a current LLM with a fixed zero-shot prompt
classify the first 50 eligible labelled Java comments, compared with
the paper's results, and which classes does it get wrong?

RQ2: For the first ten comments the model flags as smells, how has
later code evolution changed the correct label and the model's
errors, and which repair (no change / comment fix / refactor) is
justified in current code?

## Sample and method

We will use cases dataset:000001–dataset:000050, listed in
inputs/sample.csv. These are the first 50 eligible cases selected
in stable order by scripts/prepare_inputs.py. All come from
AnkiDroid's Preferences.java.

We will manually submit the five prepared batches to GPT-6 with
High thinking in ChatGPT, using the same model and settings throughout.

Each batch will use a fresh chat with memory and custom instructions
disabled. We will provide only the batch text, without reference
labels or previous answers, and use no browsing or other tools.

We will save the complete first responses unchanged in
runs/run_01/batch_01.txt through batch_05.txt. We will record the
operator, dates, displayed model and settings. Any failed attempt
or rerun will be retained and explained; we will not select answers
based on their scores.

The sample and prompt will remain unchanged after collection starts.

## Scoring and comparison

scripts/score.py compares the responses with reference/labels.csv.
It reports accuracy, MCC, per-class precision, recall and F1, a
confusion matrix and individual predictions.

Our tracker specifies comparison with the paper's o3-mini zero-shot
median accuracy of 0.72 and MCC of 0.51 (Table IV):

- REPRODUCED: accuracy is 0.62–0.82 and MCC is 0.41–0.61,
  including the endpoints.
- NOT REPRODUCED: a complete valid run falls outside either range.
- INCONCLUSIVE: responses are missing or invalid, including
  duplicate or unexpected case IDs.

The ±0.10 tolerance is our group's exploratory comparison rule.
It is not supplied by the paper or a statistical equivalence test.
Meeting it means agreement with our chosen ranges, rather than
an exact replication. Scores above the ranges also fall outside
this two-sided rule.

## Expected results

We expect accuracy within the range, but MCC below 0.51 and likely
outside the range. The sample is concentrated in Obvious and
Not a smell comments from one file. We expect most justified
repairs to involve comments only.

These are expectations recorded before running the experiment.

## Evolution and repair review

From a complete valid run, we will review the first ten comments
predicted to contain smells, in sample order, including false
positives. If fewer than ten are flagged, we will review all of them.

For each case, we will compare the original comment and code with
current code at a recorded commit. We will check whether the label
has changed and whether the original prediction remains correct
against the reviewed current label. This does not involve running
the model again on current code.

We will record a comment fix, justified refactoring or no change,
with supporting code evidence and applicable tests. Removed or
unmappable cases will be recorded rather than replaced.

## Evidence and limitations

We will retain the sample IDs, source versions/access dates, fixed
prompt, raw responses, run details, scoring output and test evidence.
We will record the final plan commit and PLAN_FROZEN tag before
collecting responses.

The sample covers one file and has few or no examples of some
categories, limiting what we can conclude. ChatGPT responses may
vary, and some comments may not map to current code.

The original M1 plan and the change from Random Forest to an LLM
remain part of the project history:
https://github.com/seancoughlan29/cs4928-g12

Any changes after freezing will be recorded with their date and reason.
Required contribution and assistance notes will be kept with the
course evidence.