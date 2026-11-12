"""Flag comments that name a code identifier which no longer exists in the file.

An IDE rename updates code but not comment text, so a comment that names a
method, field or type can silently go out of date. This check lists every
identifier a comment names and reports those that are missing from the code.

Usage: python3 scripts/check_comment_refs.py FILE.java [--json]
Exit code 1 if any comment names an identifier missing from the code.
"""
import json
import re
import sys
from pathlib import Path

GLOSSARY = Path(__file__).resolve().parent / "comment_glossary.txt"

# Words in a comment that look like code: camelCase, CamelCase with 2+ capitals,
# snake_case, or anything followed by "()".
REF = re.compile(r"\b([a-z]+[A-Z]\w*|[A-Z][a-z0-9]+[A-Z]\w*|\w+_\w+)\b|\b(\w+)\(\)")


def split_java(text):
    """Return (code_without_comments_or_strings, [(line, comment_text)])."""
    code, comments, strings = [], [], []
    i, line, n = 0, 1, len(text)
    while i < n:
        c = text[i]
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j == -1 else j
            comments.append((line, text[i + 2:j].strip()))
            i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j == -1 else j + 2
            body = text[i:j]
            comments.append((line, re.sub(r"^\s*/?\*+/?|\*+/$", "", body, flags=re.M).strip()))
            code.append("\n" * body.count("\n"))
            line += body.count("\n")
            i = j
        elif c in "\"'":
            j = i + 1
            while j < n and text[j] != c:
                j += 2 if text[j] == "\\" else 1
            code.append(" ")
            strings.append(text[i + 1:j])
            i = j + 1
        else:
            if c == "\n":
                line += 1
            code.append(c)
            i += 1
    return "".join(code), comments, " ".join(strings)


def check(path):
    code, comments, strings = split_java(Path(path).read_text(encoding="utf-8"))
    # Names that legitimately appear in comments without being identifiers in this file.
    known = set(GLOSSARY.read_text(encoding="utf-8").split()) if GLOSSARY.exists() else set()
    identifiers = set(re.findall(r"[A-Za-z_]\w*", code + " " + strings)) | known
    report = []
    for line, text in comments:
        refs = sorted({a or b for a, b in REF.findall(text)})
        if refs:
            report.append({"line": line, "comment": text[:120], "names": refs,
                           "missing": [r for r in refs if r not in identifiers]})
    return {"file": str(path), "comments": len(comments),
            "comments_naming_identifiers": len(report),
            "dangling": [r for r in report if r["missing"]], "naming": report}


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 scripts/check_comment_refs.py FILE.java [--json]")
    result = check(sys.argv[1])
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['file']}: {result['comments']} comments, "
              f"{result['comments_naming_identifiers']} name identifiers, {len(result['dangling'])} dangling")
        for r in result["dangling"]:
            print(f"  line {r['line']}: missing {r['missing']}  // {r['comment']}")
    sys.exit(1 if result["dangling"] else 0)


if __name__ == "__main__":
    main()
