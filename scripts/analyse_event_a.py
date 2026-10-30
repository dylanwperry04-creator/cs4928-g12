"""Audit Event A's saved run without altering its frozen scorer or inputs.

Usage: python scripts/analyse_event_a.py event_a/runs/run_01
Run score_event_a.py first. Supplemental outputs are deterministic.
"""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from score import LABELS, TOLERANCE, decide, mcc, read_response

ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT / "event_a"
COLLECTION_COMMIT = "b872489ab9580c83f26e7169870f6c5fe73905e5"


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def input_cases(folder):
    prompt = (ROOT / "prompts/detection_prompt.txt").read_text(encoding="utf-8")
    batches = {}
    for path in sorted(folder.glob("batch_*.txt")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith(prompt):
            raise ValueError(f"Fixed prompt differs in {path}")
        batches[path.name] = json.loads(text[len(prompt):])
    return batches


def responses(run, batches):
    expected_names = set(batches)
    actual_names = {p.name for p in run.glob("batch_*.txt")}
    if actual_names != expected_names:
        raise ValueError(f"Batch filenames differ: {actual_names ^ expected_names}")
    answers = {}
    keys = {"case_id", "predicted_label", "context_sufficient", "reason"}
    for name, cases in batches.items():
        items = read_response(run / name)
        if not isinstance(items, list) or [a.get("case_id") for a in items] != [c["case_id"] for c in cases]:
            raise ValueError(f"Case IDs or order differ in {name}")
        for item in items:
            cid = item["case_id"]
            if cid in answers or set(item) != keys:
                raise ValueError(f"Duplicate ID or wrong fields: {cid}")
            if item["predicted_label"] not in LABELS or type(item["context_sufficient"]) is not bool:
                raise ValueError(f"Invalid label or boolean: {cid}")
            if not isinstance(item["reason"], str) or not item["reason"].strip():
                raise ValueError(f"Empty or invalid reason: {cid}")
            answers[cid] = item
    return answers


def normalized_context(case):
    return [line.split(": ", 1)[1].strip() for line in case["code_context"].splitlines()
            if line.split(": ", 1)[1].strip()]


def calculate(ids, truth, answers):
    expected = [truth[c] for c in ids]
    predicted = [answers[c]["predicted_label"] for c in ids]
    correct = sum(t == p for t, p in zip(expected, predicted))
    return {"n": len(ids), "correct": correct, "accuracy": correct / len(ids),
            "mcc": mcc(expected, predicted)}


def write_csv(path, rows, fields=None):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(run):
    run = (ROOT / run).resolve()
    out = EVENT / "results" / run.name
    frozen = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    old_batches = input_cases(ROOT / "inputs")
    new_batches = input_cases(EVENT / "inputs")
    old_cases = {c["case_id"]: c for batch in old_batches.values() for c in batch}
    new_cases = {c["case_id"]: c for batch in new_batches.values() for c in batch}
    old_answers = responses(ROOT / "runs/run_01", old_batches)
    new_answers = responses(run, new_batches)
    truth = {r["case_id"]: r["label"] for r in read_csv(ROOT / "reference/labels.csv")}
    event_truth = {r["case_id"]: r["label"] for r in read_csv(EVENT / "reference_labels.csv")}
    if event_truth != {c: truth[c] for c in new_cases}:
        raise ValueError("Event labels differ from inherited M2 labels")
    mapping = {r["case_id"]: r for r in read_csv(EVENT / "mapping.csv")}
    review = read_csv(EVENT / "review/comment_review.csv")
    if len(review) != len(mapping) or {r["case_id"] for r in review} != set(mapping):
        raise ValueError("Review must cover every original case exactly once")

    ids = list(event_truth)
    full = calculate(list(truth), truth, old_answers)
    matched = calculate(ids, truth, old_answers)
    event = calculate(ids, truth, new_answers)
    if (round(event["accuracy"], 3) != frozen["event_a_all_survivors"]["accuracy"]
            or round(event["mcc"], 3) != frozen["event_a_all_survivors"]["mcc"]):
        raise ValueError("Recomputed scores disagree with frozen first result")

    unchanged = [c for c in ids if mapping[c]["status"] == "unchanged"]
    flips = [c for c in unchanged if old_answers[c]["predicted_label"] != new_answers[c]["predicted_label"]]
    full_context_equal = [c for c in unchanged if normalized_context(old_cases[c]) == normalized_context(new_cases[c])]
    all_flips = [c for c in ids if old_answers[c]["predicted_label"] != new_answers[c]["predicted_label"]]
    source = (EVENT / "source/Preferences_9db834afd0.java").read_text(encoding="utf-8").splitlines()
    active_targets = [c for c in ids if not source[new_cases[c]["line_start"] - 1].lstrip().startswith(("//", "/*", "*"))]
    sensitivity = []
    for name, excluded in [
        ("frozen_all_automatic_matches", []),
        ("exclude_active_code_false_match", ["dataset:000015"]),
        ("exclude_false_match_and_ambiguous_identity", ["dataset:000015", "dataset:000043"]),
    ]:
        subset = [c for c in ids if c not in excluded]
        before, after = calculate(subset, truth, old_answers), calculate(subset, truth, new_answers)
        sensitivity.append({"analysis": name, "excluded_ids": ";".join(excluded), "n": len(subset),
                            "m2_accuracy": before["accuracy"], "m2_mcc": before["mcc"],
                            "event_a_accuracy": after["accuracy"], "event_a_mcc": after["mcc"],
                            "decision_vs_paper": decide(after["accuracy"], after["mcc"], True)})

    audit = {
        "collection_commit": COLLECTION_COMMIT,
        "raw_response_validation": {"valid": True, "batch_sizes": [len(c) for c in new_batches.values()],
                                    "unique_case_ids": len(new_answers), "fixed_prompt_identical": True},
        "full_m2": full, "m2_on_same_automatic_matches": matched, "event_a_frozen": event,
        "delta_vs_full_m2": {k: event[k] - full[k] for k in ("accuracy", "mcc")},
        "delta_vs_same_cases_m2": {k: event[k] - matched[k] for k in ("accuracy", "mcc")},
        "all_label_flip_ids": all_flips,
        "paired_changes": {
            "wrong_to_correct": [c for c in ids if old_answers[c]["predicted_label"] != truth[c] and new_answers[c]["predicted_label"] == truth[c]],
            "correct_to_wrong": [c for c in ids if old_answers[c]["predicted_label"] == truth[c] and new_answers[c]["predicted_label"] != truth[c]]},
        "unchanged_nearby_window": {
            "n": len(unchanged), "flip_ids": flips, "flip_rate": len(flips) / len(unchanged),
            "identical_full_normalized_context_ids": full_context_equal,
            "challenge_above_30_percent_triggered": len(flips) / len(unchanged) > .30},
        "pre_recorded_predictions": {
            "at_least_40_automatic_matches": len(ids) >= 40,
            "accuracy_and_mcc_within_010_of_full_m2": all(abs(event[k] - full[k]) <= TOLERANCE for k in ("accuracy", "mcc")),
            "same_cases_supplemental_within_010": all(abs(event[k] - matched[k]) <= TOLERANCE for k in ("accuracy", "mcc")),
            "score_drop_over_010_vs_full_m2": any(full[k] - event[k] > TOLERANCE for k in ("accuracy", "mcc")),
            "two_to_five_newly_stale_comments": "not_established_from_supplied_sources"},
        "mapping_audit": {"target_points_to_active_code": active_targets,
                          "ambiguous_duplicate_ids": ["dataset:000043", "dataset:000045"],
                          "manual_assessments": dict(Counter(r["mapping_review"] for r in review))},
        "source_review": {"accuracy_assessments": dict(Counter(r["still_accurate"] for r in review)),
                          "confirmed_new_stale_cases": [r["case_id"] for r in review if r["evolution_assessment"] == "newly_stale"],
                          "preexisting_misaligned_cases": [r["case_id"] for r in review if r["evolution_assessment"] == "preexisting_misalignment"],
                          "unresolved_warning_cases": [r["case_id"] for r in review if r["still_accurate"] == "uncertain"],
                          "reviewer": "ChatGPT/Codex source inspection after scoring; not blinded human annotation"},
        "paper_decision_frozen": decide(event["accuracy"], event["mcc"], True),
        "sensitivity_is_post_run": True,
    }
    (out / "audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    write_csv(out / "sensitivity.csv", sensitivity)
    comparison = [{"sample": name, **value} for name, value in [
        ("M2 full original sample", full), ("M2 same 38 automatic matches", matched), ("Event A frozen 38", event)]]
    write_csv(out / "comparison.csv", comparison)
    write_csv(out / "confusion_matrix.csv", [
        {"actual": label, **{p: sum(event_truth[c] == label and new_answers[c]["predicted_label"] == p for c in ids)
                              for p in LABELS}} for label in LABELS])
    frozen_paths = [ROOT / p for p in ("PLAN.md", "EVENT_A.md", "prompts/detection_prompt.txt",
                    "reference/labels.csv", "results/run_01/metrics.json", "results/run_01/predictions.csv",
                    "scripts/score.py", "scripts/score_event_a.py", "scripts/prepare_inputs.py", "scripts/prepare_event_a.py")]
    for folder in (ROOT / "inputs", ROOT / "runs/run_01", EVENT / "inputs", run, EVENT / "source"):
        frozen_paths.extend(p for p in folder.iterdir() if p.is_file())
    frozen_paths.extend([EVENT / "mapping.csv", EVENT / "reference_labels.csv"])
    manifest = {"collection_commit": COLLECTION_COMMIT,
                "sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(set(frozen_paths))}}
    (out / "file_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/analyse_event_a.py event_a/runs/run_01")
    main(Path(sys.argv[1]))
