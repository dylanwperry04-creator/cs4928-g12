"""Score saved LLM responses against the reference labels.

Usage: python3 scripts/score.py runs/run_01
Expects runs/run_01/batch_01.txt ... batch_05.txt, each holding the model's
reply exactly as returned. Writes everything to results/run_01/.
"""
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABELS = ["Not a smell", "Obvious", "Task", "Vague", "Beautification",
          "Commented out code", "Misleading", "Too much info", "Nonlocal info", "Irrelevant"]
INVALID = "INVALID"

# Decision rule (see PLAN.md): compare with the paper's o3-mini zero-shot median.
PAPER_ACCURACY = 0.72
PAPER_MCC = 0.51
TOLERANCE = 0.10


def read_response(path):
    text = path.read_text(encoding="utf-8-sig").strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


def mcc(truth, pred):
    n = len(truth)
    correct = sum(t == p for t, p in zip(truth, pred))
    t_count, p_count = Counter(truth), Counter(pred)
    classes = set(t_count) | set(p_count)
    top = correct * n - sum(t_count[k] * p_count[k] for k in classes)
    bottom = math.sqrt((n * n - sum(v * v for v in p_count.values())) *
                       (n * n - sum(v * v for v in t_count.values())))
    return top / bottom if bottom else 0.0


def per_class(truth, pred):
    rows = []
    for label in LABELS:
        tp = sum(t == label and p == label for t, p in zip(truth, pred))
        fp = sum(t != label and p == label for t, p in zip(truth, pred))
        fn = sum(t == label and p != label for t, p in zip(truth, pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * tp / (2 * tp + fp + fn) if tp + fp + fn else 0.0
        rows.append({"label": label, "support": tp + fn, "precision": round(precision, 3),
                     "recall": round(recall, 3), "f1": round(f1, 3)})
    return rows


def decide(accuracy, mcc_value, all_valid):
    if not all_valid:
        return "INCONCLUSIVE"
    def within(value, target):
        difference = abs(value - target)
        return difference <= TOLERANCE or math.isclose(difference, TOLERANCE, rel_tol=0.0, abs_tol=1e-12)
    ok = within(accuracy, PAPER_ACCURACY) and within(mcc_value, PAPER_MCC)
    return "REPRODUCED" if ok else "NOT REPRODUCED"


def main(run_dir):
    run_dir = Path(run_dir)
    out = ROOT / "results" / run_dir.name
    if out.exists():
        sys.exit(f"{out} already exists. Use a new run name; never overwrite results.")

    with open(ROOT / "reference" / "labels.csv", encoding="utf-8") as f:
        truth_by_id = {r["case_id"]: r["label"] for r in csv.DictReader(f)}

    def incomplete(message):
        out.mkdir(parents=True)
        result = {"run": run_dir.name, "decision": "INCONCLUSIVE", "issue": message}
        (out / "metrics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))

    answers = {}
    try:
        for i in range(1, 6):
            items = read_response(run_dir / f"batch_{i:02d}.txt")
            if not isinstance(items, list):
                raise ValueError("Each response must be a JSON array")
            for item in items:
                if not isinstance(item, dict):
                    raise ValueError("Each answer must be a JSON object")
                cid = item.get("case_id")
                if not isinstance(cid, str) or cid not in truth_by_id:
                    raise ValueError(f"Unexpected case ID: {cid!r}")
                if cid in answers:
                    raise ValueError(f"Duplicate answer for {cid}")
                if set(item) != {"case_id", "predicted_label", "context_sufficient", "reason"}:
                    raise ValueError(f"Incorrect answer fields for {cid}")
                if not isinstance(item["predicted_label"], str) or not isinstance(item["reason"], str) or not isinstance(item["context_sufficient"], bool):
                    raise ValueError(f"Incorrect answer field types for {cid}")
                answers[cid] = item
        missing = [cid for cid in truth_by_id if cid not in answers]
        if missing:
            raise ValueError(f"Missing answers for: {missing}")
    except (OSError, ValueError, IndexError) as exc:
        incomplete(str(exc))
        return

    ids = list(truth_by_id)
    truth = [truth_by_id[c] for c in ids]
    pred = [answers[c]["predicted_label"] if answers[c]["predicted_label"] in LABELS else INVALID for c in ids]
    accuracy = sum(t == p for t, p in zip(truth, pred)) / len(ids)
    mcc_value = mcc(truth, pred)
    classes = per_class(truth, pred)
    supported = [r for r in classes if r["support"]]
    all_valid = INVALID not in pred
    result = {
        "run": run_dir.name,
        "n": len(ids),
        "accuracy": round(accuracy, 3),
        "mcc": round(mcc_value, 3),
        "macro_f1_all_10_labels": round(sum(r["f1"] for r in classes) / len(classes), 3),
        "macro_f1_labels_present": round(sum(r["f1"] for r in supported) / len(supported), 3),
        "invalid_outputs": pred.count(INVALID),
        "paper_target": {"accuracy": PAPER_ACCURACY, "mcc": PAPER_MCC, "tolerance": TOLERANCE},
        "decision": decide(accuracy, mcc_value, all_valid),
    }

    out.mkdir(parents=True)
    (out / "metrics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    with open(out / "per_class.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(classes[0]))
        w.writeheader()
        w.writerows(classes)
    with open(out / "predictions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "label", "predicted", "correct", "context_sufficient", "reason"])
        for c, t, p in zip(ids, truth, pred):
            w.writerow([c, t, p, t == p, answers[c].get("context_sufficient"), answers[c].get("reason", "")])
    cols = LABELS + ([INVALID] if not all_valid else [])
    with open(out / "confusion_matrix.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["actual \\ predicted"] + cols)
        for a in LABELS:
            w.writerow([a] + [sum(t == a and p == b for t, p in zip(truth, pred)) for b in cols])
    # RQ2: first ten cases the model flagged as a smell, in sample order (false positives included).
    flagged = [(c, t, p) for c, t, p in zip(ids, truth, pred) if p not in ("Not a smell", INVALID)][:10]
    with open(out / "repair_candidates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "label", "predicted", "false_positive"])
        for c, t, p in flagged:
            w.writerow([c, t, p, t == "Not a smell"])

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/score.py runs/<run_name>")
    main(sys.argv[1])
