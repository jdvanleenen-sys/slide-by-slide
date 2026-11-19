"""Tests for _tools/deck.py and _tools/check_walkthrough.py, including the planted invented number.

    python -m unittest discover -s tests
"""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLANTED = Path(__file__).resolve().parent / "planted"


def load(name):
    spec = importlib.util.spec_from_file_location(name, REPO / "_tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


deck = load("deck")
checker = load("check_walkthrough")


class Workspace(unittest.TestCase):
    """Each test gets a fresh copy of deck/ and empty my-work/ and my-project/ folders."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / "deck", self.root / "deck")
        (self.root / "my-work").mkdir()
        (self.root / "my-project").mkdir()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def use(self, walkthrough, me="me.md"):
        shutil.copy(PLANTED / walkthrough, self.root / "my-work" / "walkthrough.md")
        shutil.copy(PLANTED / me, self.root / "my-work" / "me.md")


class DeckTests(Workspace):
    def test_sample_deck_starts_at_slide_1(self):
        self.assertIn("slides: 3 | done: 0 | skipped: 0 | next: 1", deck.status(self.root))

    def test_next_moves_past_done_and_skipped(self):
        self.use("clean.md")
        self.assertIn("done: 1 | skipped: 1 | next: 3", deck.status(self.root))

    def test_show_md_slide_has_text_and_notes(self):
        out = deck.show(self.root, 1)
        self.assertTrue(out.startswith("Slide 1: Who has the problem?"))
        self.assertIn("Notes:", out)

    def test_show_missing_slide_says_so(self):
        self.assertIn("There is no slide 9", deck.show(self.root, 9))

    def test_empty_deck_asks_for_inputs(self):
        (self.root / "deck" / "slides.md").unlink()
        self.assertIn("Add the slides through Inputs", deck.status(self.root))

    def test_pdf_deck_wins_and_renders_a_picture(self):
        try:
            import pymupdf
        except ImportError:
            self.skipTest("PyMuPDF not installed")
        doc = pymupdf.open()
        for text in ("First slide", "Second slide"):
            doc.new_page().insert_text((72, 72), text)
        doc.save(self.root / "deck" / "course.pdf")
        doc.close()
        self.assertIn("deck: deck/course.pdf | slides: 2", deck.status(self.root))
        out = deck.show(self.root, 2)
        self.assertIn("picture: my-work/slides/slide-2.png", out)
        self.assertTrue((self.root / "my-work" / "slides" / "slide-2.png").exists())


class CheckTests(Workspace):
    def test_clean_walkthrough_passes(self):
        self.use("clean.md")
        self.assertEqual(checker.check(self.root), [])

    def test_planted_invented_number_is_caught(self):
        self.use("invented-number.md")
        problems = checker.check(self.root)
        self.assertEqual(len(problems), 1)
        self.assertIn("slide 3: Decided has 5000", problems[0])

    def test_math_shown_result_is_allowed(self):
        self.use("math-shown.md")
        self.assertEqual(checker.check(self.root), [])

    def test_empty_answer_fails(self):
        self.use("no-answer.md")
        self.assertEqual(checker.check(self.root), ["slide 1: no answer written"])

    def test_number_from_my_project_is_allowed(self):
        self.use("project-number.md")
        (self.root / "my-project" / "prices.md").write_text("Rate: $85 an hour\n", encoding="utf-8")
        self.assertEqual(checker.check(self.root), [])

    def test_no_walkthrough_yet(self):
        self.assertIn("run setup first", checker.check(self.root)[0])


if __name__ == "__main__":
    unittest.main()
