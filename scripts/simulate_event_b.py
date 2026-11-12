"""Event B: simulate public API renames and measure comment drift.

Builds two states of the 2022 Preferences.java:
  S0  original 2022 file
  S1  Week 9 design applied (comments for cases 000006 and 000011 deleted)
then applies IDE-style renames (code tokens renamed, comments and strings untouched)
and runs scripts/check_comment_refs.py on each result.

Usage: python3 scripts/simulate_event_b.py
Writes event_b/states/*.java and event_b/results.json
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_comment_refs import check  # noqa: E402

SOURCE = ROOT / "event_a" / "source" / "Preferences_9db834afd0.java"
OUT = ROOT / "event_b"

# Week 9 decision (README, commit 41a203a): delete these two standalone comment lines.
WEEK9_DELETIONS = {210: "// Add a home button to the actionbar", 890: "// Build languages"}

# Public API/type renames. Each renames a method used in the code; R1 and R2 are named
# by comments in our 50-comment sample, R3 is the ActionBar to Toolbar direction the
# 2022 code is already moving in (enableToolbar()).
RENAMES = {
    "R1_modSchemaNoCheck": ("modSchemaNoCheck", "modSchemaWithoutConfirmation"),
    "R2_onRestoreInstanceState": ("onRestoreInstanceState", "onRestoreSavedState"),
    "R3_getSupportActionBar": ("getSupportActionBar", "getSupportToolbar"),
}


def week9(lines):
    out = []
    for n, l in enumerate(lines, 1):
        if n in WEEK9_DELETIONS:
            assert l.strip() == WEEK9_DELETIONS[n], (n, l)
            continue
        out.append(l)
    return out


def ide_rename(text, old, new):
    """Rename a token in code only, leaving comments and string literals alone."""
    out, i, n = [], 0, len(text)
    token = re.compile(rf"\b{re.escape(old)}\b")
    while i < n:
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j == -1 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j == -1 else j + 2
        elif text[i] in "\"'":
            j = i + 1
            while j < n and text[j] != text[i]:
                j += 2 if text[j] == "\\" else 1
            j += 1
        else:
            m = re.compile(r"//|/\*|[\"']").search(text, i)
            j = m.start() if m else n
            out.append(token.sub(new, text[i:j]))
            i = j
            continue
        out.append(text[i:j])
        i = j
    return "".join(out)


def mentions(text, word):
    """Comment lines that mention a word in plain English (not caught by the checker)."""
    return [n for n, l in enumerate(text.splitlines(), 1)
            if "//" in l and word.lower() in l.split("//", 1)[1].lower().replace(" ", "")]


def main():
    s0 = SOURCE.read_text(encoding="utf-8")
    s1 = "\n".join(week9(s0.splitlines())) + "\n"
    states = OUT / "states"
    states.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, text in (("S0_original", s0), ("S1_week9", s1)):
        (states / f"{name}.java").write_text(text, encoding="utf-8")
        base = check(states / f"{name}.java")
        row = {"comments": base["comments"], "naming_identifiers": base["comments_naming_identifiers"],
               "dangling_before_rename": [(d["line"], d["missing"]) for d in base["dangling"]],
               "renames": {}}
        for key, (old, new) in RENAMES.items():
            renamed = ide_rename(text, old, new)
            path = states / f"{name}__{key}.java"
            path.write_text(renamed, encoding="utf-8")
            after = check(path)
            new_dangling = [(d["line"], d["missing"], d["comment"][:80]) for d in after["dangling"]
                            if (d["line"], d["missing"]) not in row["dangling_before_rename"]]
            row["renames"][key] = {
                "code_lines_changed": sum(a != b for a, b in zip(text.splitlines(), renamed.splitlines())),
                "comments_flagged_by_check": new_dangling,
                "comments_mentioning_old_concept_in_plain_words": mentions(renamed, "actionbar") if key.startswith("R3") else [],
            }
        results[name] = row
    (OUT / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for name, row in results.items():
        print(f"{name}: {row['comments']} comments, {row['naming_identifiers']} name identifiers, "
              f"{len(row['dangling_before_rename'])} dangling before rename")
        for key, r in row["renames"].items():
            print(f"  {key}: {r['code_lines_changed']} code lines changed, "
                  f"{len(r['comments_flagged_by_check'])} comments flagged, "
                  f"plain-word mentions: {r['comments_mentioning_old_concept_in_plain_words']}")
            for f in r["comments_flagged_by_check"]:
                print("     ", f)


if __name__ == "__main__":
    main()
