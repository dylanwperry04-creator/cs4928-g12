"""Checks for the comment-reference check. Run: python3 -m unittest discover tests"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_comment_refs import check  # noqa: E402
from simulate_event_b import ide_rename  # noqa: E402


def run(java):
    with tempfile.NamedTemporaryFile("w", suffix=".java", delete=False) as f:
        f.write(java)
    return check(f.name)


class CommentRefTests(unittest.TestCase):
    def test_comment_naming_existing_method_is_fine(self):
        r = run("void f() {\n  // we called resetCache() first\n  resetCache();\n}\n")
        self.assertEqual(r["comments_naming_identifiers"], 1)
        self.assertEqual(r["dangling"], [])

    def test_rename_leaves_comment_dangling(self):
        java = "void f() {\n  // we called resetCache() first\n  resetCache();\n}\n"
        renamed = ide_rename(java, "resetCache", "clearCache")
        self.assertIn("// we called resetCache() first", renamed)
        self.assertIn("  clearCache();", renamed)
        self.assertEqual(run(renamed)["dangling"][0]["missing"], ["resetCache"])

    def test_names_inside_strings_count_as_known(self):
        r = run('void f() {\n  // reads the "estTimes" key\n  get("estTimes");\n}\n')
        self.assertEqual(r["dangling"], [])

    def test_plain_english_is_not_flagged(self):
        r = run("void f() {\n  // add a home button to the actionbar\n  x();\n}\n")
        self.assertEqual(r["comments_naming_identifiers"], 0)


if __name__ == "__main__":
    unittest.main()
