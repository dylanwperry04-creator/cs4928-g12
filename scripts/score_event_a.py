"""Score the Event A run with the unchanged M2 scorer, then compare with M2.

Usage: python3 scripts/score_event_a.py event_a/runs/run_01
Expects batch_01.txt ... batch_NN.txt (one per file in event_a/inputs/).
Writes event_a/results/<run>/.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from score import LABELS, INVALID, read_response, mcc, per_class, decide  # noqa: E402

EVENT = ROOT / "event_a"


def metrics(truth, pred):
    if not truth:
        return {"n": 0}
    return {"n": len(truth),
            "accuracy": round(sum(t == p for t, p in zip(truth, pred)) / len(truth), 3),
            "mcc": round(mcc(truth, pred), 3)}


def main(run_dir):
    run_dir = Path(run_dir)
    out = EVENT / "results" / run_dir.name
    if out.exists():
        sys.exit(f"{out} already exists. Use a new run name; never overwrite results.")

    with open(EVENT / "reference_labels.csv", encoding="utf-8") as f:
        truth_by_id = {r["case_id"]: r["label"] for r in csv.DictReader(f)}
    with open(EVENT / "mapping.csv", encoding="utf-8") as f:
        status = {r["case_id"]: r["status"] for r in csv.DictReader(f)}
    with open(ROOT / "results" / "run_01" / "predictions.csv", encoding="utf-8") as f:
        m2_pred = {r["case_id"]: r["predicted"] for r in csv.DictReader(f)}

    answers = {}
    for path in sorted((EVENT / "inputs").glob("batch_*.txt")):
        for item in read_response(run_dir / path.name):
            cid = item["case_id"]
            if cid not in truth_by_id or cid in answers:
                sys.exit(f"Unexpected or duplicate case ID: {cid}")
            answers[cid] = item
    missing = [c for c in truth_by_id if c not in answers]
    if missing:
        sys.exit(f"Missing answers for: {missing}")

    ids = list(truth_by_id)
    truth = [truth_by_id[c] for c in ids]
    pred = [answers[c]["predicted_label"] if answers[c]["predicted_label"] in LABELS else INVALID for c in ids]
    acc = sum(t == p for t, p in zip(truth, pred)) / len(ids)
    mcc_value = mcc(truth, pred)

    def subset(kind):
        sel = [i for i, c in enumerate(ids) if status[c] == kind]
        return metrics([truth[i] for i in sel], [pred[i] for i in sel])

    def agreement(kind=None):
        sel = [c for c, p in zip(ids, pred) if kind is None or status[c] == kind]
        same = sum(answers[c]["predicted_label"] == m2_pred[c] for c in sel)
        return {"n": len(sel), "same_label_as_m2": same, "rate": round(same / len(sel), 3) if sel else None}

    m2_same_cases = [c for c in ids]
    m2_truth = [truth_by_id[c] for c in m2_same_cases]
    m2_on_survivors = metrics(m2_truth, [m2_pred[c] for c in m2_same_cases])

    result = {
        "run": run_dir.name,
        "comments_in_m2_sample": len(status),
        "survived": len(ids),
        "removed": sum(s == "removed" for s in status.values()),
        "event_a_all_survivors": {"n": len(ids), "accuracy": round(acc, 3), "mcc": round(mcc_value, 3),
                                  "invalid_outputs": pred.count(INVALID),
                                  "decision_vs_paper": decide(acc, mcc_value, INVALID not in pred)},
        "event_a_nearby_code_unchanged": subset("unchanged"),
        "event_a_nearby_code_changed": subset("code_changed"),
        "m2_on_same_survivors": m2_on_survivors,
        "label_agreement_with_m2": {"all": agreement(), "unchanged": agreement("unchanged"),
                                    "code_changed": agreement("code_changed")},
    }

    out.mkdir(parents=True)
    (out / "metrics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    classes = per_class(truth, pred)
    with open(out / "per_class.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(classes[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(classes)
    with open(out / "predictions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["case_id", "status", "label", "m2_predicted", "event_a_predicted", "changed_from_m2",
                    "context_sufficient", "reason"])
        for c, t, p in zip(ids, truth, pred):
            w.writerow([c, status[c], t, m2_pred[c], p, p != m2_pred[c],
                        answers[c].get("context_sufficient"), answers[c].get("reason", "")])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/score_event_a.py event_a/runs/<run_name>")
    main(sys.argv[1])
