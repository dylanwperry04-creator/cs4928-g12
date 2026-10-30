"""Event A: find the 50 M2 comments in a later version of the same file and
build model inputs using the unchanged M2 prompt and context window.

Usage: python3 scripts/prepare_event_a.py
Reads  event_a/source/Preferences_79163e4b57.java  (M2 snapshot, 4 May 2021)
       event_a/source/Preferences_9db834afd0.java  (later snapshot, 28 Feb 2022)
Writes event_a/mapping.csv, event_a/reference_labels.csv,
       event_a/inputs/batch_XX.txt
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_inputs import DATASET, PROMPT, LINES_BEFORE, LINES_AFTER, BATCH_SIZE, SAMPLE_SIZE, eligible_cases  # noqa: E402

OLD = ROOT / "event_a" / "source" / "Preferences_79163e4b57.java"
NEW = ROOT / "event_a" / "source" / "Preferences_9db834afd0.java"
NEAR = 3
NEW_PATH = "/AnkiDroid/src/main/java/com/ichi2/anki/Preferences.java"


def squash(text):
    """Compare comment text ignoring whitespace and comment markers."""
    return re.sub(r"\s+|//|/\*|\*/|\*", "", text)


def context(lines, start, end):
    lo = max(1, start - LINES_BEFORE)
    hi = min(len(lines), end + LINES_AFTER)
    return lo, hi, "\n".join(f"{i}: {lines[i - 1]}" for i in range(lo, hi + 1))


def code_only(lines, lo, hi):
    return [l.strip() for l in lines[lo - 1:hi] if l.strip()]


def find(comment, lines, start_hint, used):
    """Return (start, end) of the comment in lines, nearest to start_hint, or None."""
    target = squash(comment)
    height = comment.count("\n") + 1
    hits = []
    for i in range(len(lines)):
        for h in (height, height + 1, height + 2):
            block = lines[i:i + h]
            if target and target in squash("\n".join(block)) and target not in squash("\n".join(block[1:])):
                if (i + 1) not in used:
                    hits.append((i + 1, i + h))
                break
    if not hits:
        return None
    return min(hits, key=lambda s: abs(s[0] - start_hint))


def main():
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    sample = eligible_cases(data)[:SAMPLE_SIZE]
    old = OLD.read_text(encoding="utf-8").splitlines()
    new = NEW.read_text(encoding="utf-8").splitlines()
    scale = len(new) / len(old)

    rows, cases, used = [], [], set()
    for c in sample:
        hit = find(c["comment"], new, int(c["line_start"] * scale), used)
        row = {"case_id": c["case_id"], "label": c["label"], "old_lines": f"{c['line_start']}-{c['line_end']}",
               "new_lines": "", "status": "removed"}
        if hit:
            used.add(hit[0])
            s, e = hit
            nlo, nhi, ctx = context(new, s, e)
            # "Unchanged" means the code right next to the comment (3 lines either side) is identical.
            near_old = code_only(old, max(1, c["line_start"] - NEAR), min(len(old), c["line_end"] + NEAR))
            near_new = code_only(new, max(1, s - NEAR), min(len(new), e + NEAR))
            same = near_old == near_new
            row.update(new_lines=f"{s}-{e}", status="unchanged" if same else "code_changed")
            cases.append({"case_id": c["case_id"], "project": c["project"], "file_path": NEW_PATH,
                          "line_start": s, "line_end": e, "comment": c["comment"], "code_context": ctx,
                          "label": c["label"]})
        rows.append(row)

    out = ROOT / "event_a"
    (out / "inputs").mkdir(parents=True, exist_ok=True)
    with open(out / "mapping.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(out / "reference_labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["case_id", "label"])
        for c in cases:
            w.writerow([c["case_id"], c["label"]])
    prompt = PROMPT.read_text(encoding="utf-8")
    keys = ["case_id", "project", "file_path", "line_start", "line_end", "comment", "code_context"]
    for b in range(0, len(cases), BATCH_SIZE):
        batch = [{k: c[k] for k in keys} for c in cases[b:b + BATCH_SIZE]]
        path = out / "inputs" / f"batch_{b // BATCH_SIZE + 1:02d}.txt"
        path.write_bytes((prompt + json.dumps(batch, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

    counts = {s: sum(r["status"] == s for r in rows) for s in ("unchanged", "code_changed", "removed")}
    print(f"{len(cases)} of {len(sample)} comments found in later snapshot: {counts}")
    print(f"{(len(cases) + BATCH_SIZE - 1) // BATCH_SIZE} batches written to event_a/inputs/")


if __name__ == "__main__":
    main()
