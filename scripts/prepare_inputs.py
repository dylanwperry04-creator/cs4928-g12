"""Build the 50-case sample and the five model input batches from dataset.json.

Usage: python3 scripts/prepare_inputs.py
Writes inputs/sample.csv, inputs/batch_01.txt ... batch_05.txt and
reference/labels.csv. Running it again gives byte-identical files.
"""
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "original_artefact" / "dataset.json"
PROMPT = ROOT / "prompts" / "detection_prompt.txt"

LABELS = ["Not a smell", "Obvious", "Task", "Vague", "Beautification",
          "Commented out code", "Misleading", "Too much info", "Nonlocal info", "Irrelevant"]
SAMPLE_SIZE = 50
BATCH_SIZE = 10
LINES_BEFORE = 20
LINES_AFTER = 30


def eligible_cases(data):
    """Number every comment in file order, then keep the eligible Java ones."""
    cases = []
    number = 0
    for project, files in data.items():
        for file_path, info in files.items():
            source = unquote(info["source_code"])
            lines = source.splitlines()
            for index, c in enumerate(info["comments"]):
                number += 1
                start, end = c["pos_begin"], c["pos_end"]
                if not file_path.endswith(".java"):
                    continue
                if not c["comment"].strip() or c["label"] not in LABELS:
                    continue
                if not (isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= len(lines)):
                    continue
                lo = max(1, start - LINES_BEFORE)
                hi = min(len(lines), end + LINES_AFTER)
                cases.append({
                    "case_id": f"dataset:{number:06d}",
                    "project": project,
                    "file_path": file_path,
                    "comment_index": index,
                    "line_start": start,
                    "line_end": end,
                    "comment": c["comment"],
                    "code_context": "\n".join(f"{i}: {lines[i - 1]}" for i in range(lo, hi + 1)),
                    "label": c["label"],
                    "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
                })
    cases.sort(key=lambda c: (c["case_id"], c["file_path"], c["comment_index"]))
    return cases


def main():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    sample = eligible_cases(data)[:SAMPLE_SIZE]

    with open(ROOT / "inputs" / "sample.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "project", "file_path", "line_start", "line_end", "source_sha256"])
        for c in sample:
            w.writerow([c["case_id"], c["project"], c["file_path"], c["line_start"], c["line_end"], c["source_sha256"]])

    with open(ROOT / "reference" / "labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "label"])
        for c in sample:
            w.writerow([c["case_id"], c["label"]])

    prompt = PROMPT.read_text(encoding="utf-8")
    keys = ["case_id", "project", "file_path", "line_start", "line_end", "comment", "code_context"]
    for b in range(0, SAMPLE_SIZE, BATCH_SIZE):
        batch = [{k: c[k] for k in keys} for c in sample[b:b + BATCH_SIZE]]
        out = ROOT / "inputs" / f"batch_{b // BATCH_SIZE + 1:02d}.txt"
        out.write_bytes((prompt + json.dumps(batch, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

    print(f"{len(sample)} cases written to inputs/ ({SAMPLE_SIZE // BATCH_SIZE} batches)")


if __name__ == "__main__":
    main()
