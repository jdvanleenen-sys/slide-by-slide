"""Tests for the v1.1 fixes: open the slide, slide numbers count as given, question shape, HTML import.

    python -m unittest discover -s tests
"""
import importlib.util
import unittest

from test_tools import REPO, Workspace, checker, deck

_spec = importlib.util.spec_from_file_location("import_html", REPO / "_tools" / "import_html.py")
importer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(importer)

HEAD = "# Walkthrough\n\n---\n\n"
ME = "# Me\n- **Numbers I have given (as I said them):** not given\n"
HTML = """<html><head><style>.slide{color:red}</style></head><body>
<section class="slide " id="slide-1" data-title="Cover"><h1>When the checker is the target</h1>
<p>Two studies, one question.</p><aside hidden>SAY: welcome everyone.</aside></section>
<section class="slide"><h2>Study 2</h2><p>Planted<br>attacks</p><script>var x = 1;</script></section>
</body></html>"""


def entry(n, title, question, project="none", decided="nothing yet"):
    return (f"## Slide {n}: {title}\n- **Point:** p\n- **For my project:** {project}\n"
            f"- **Question:** {question}\n- **My answer:** a\n- **Decided:** {decided}\n"
            f"- **Follow-up:** none\n\n")


def pdf(root, texts):
    import pymupdf
    doc = pymupdf.open()
    for text in texts:
        page = doc.new_page()
        if text:
            page.insert_text((72, 72), text)
    doc.save(root / "deck" / "course.pdf")
    doc.close()


class Base(Workspace):
    def walk(self, *entries):
        (self.root / "my-work" / "walkthrough.md").write_text(HEAD + "".join(entries), encoding="utf-8")
        (self.root / "my-work" / "me.md").write_text(ME, encoding="utf-8")
        return checker.check(self.root)


class ShowTests(Base):
    def setUp(self):
        super().setUp()
        try:
            import pymupdf  # noqa: F401
        except ImportError:
            self.skipTest("PyMuPDF not installed")

    def test_show_open_calls_opener(self):
        pdf(self.root, ["First slide", "Second slide"])
        opened = []
        out = deck.show(self.root, 2, opened.append)
        self.assertEqual([p.name for p in opened], ["slide-2.png"])
        self.assertIn("opened on screen", out)

    def test_show_without_open_does_not_open(self):
        pdf(self.root, ["First slide"])
        self.assertNotIn("opened on screen", deck.show(self.root, 1))

    def test_picture_only_slide_says_no_text(self):
        pdf(self.root, [""])
        self.assertIn("saved as pictures", deck.show(self.root, 1))


class SlideNumberTests(Base):
    def test_slide_text_number_is_given(self):
        (self.root / "deck" / "slides.md").write_text(
            "## Slide 1: Study 2 results\nThe second study planted 12 attacks.\n", encoding="utf-8")
        problems = self.walk(entry(1, "Study 2 results", "What would you plant first?",
                                   project="Study 2 used 12 attacks.", decided="Charge 5000."))
        self.assertEqual(problems, ["slide 1: Decided has 5000, which the learner never gave"])

    def test_html_deck_gets_an_import_hint(self):
        (self.root / "deck" / "slides.md").unlink()
        (self.root / "deck" / "talk.html").write_text(HTML, encoding="utf-8")
        self.assertIn("python _tools/import_html.py deck/talk.html", deck.status(self.root))


class QuestionTests(Base):
    def test_good_questions_pass(self):
        self.assertEqual(self.walk(entry(1, "A", "Who has the problem?"),
                                   entry(2, "B", "What does it cost them?")), [])

    def test_repeat_question_fails(self):
        problems = self.walk(entry(1, "A", "What does it cost them?"), entry(2, "B", "Who is it?"),
                             entry(3, "C", "what does it cost them"))
        self.assertEqual(problems, ["slide 3: Question repeats one of the last three"])

    def test_repeat_older_than_three_passes(self):
        qs = ["What does it cost?", "Who is it?", "When is it due?", "Where is it?", "What does it cost?"]
        self.assertEqual(self.walk(*(entry(i, "T", q) for i, q in enumerate(qs, 1))), [])

    def test_yes_no_question_fails(self):
        problems = self.walk(entry(1, "A", "Is that rate still right?"))
        self.assertEqual(problems, ["slide 1: Question is a yes or no question; ask how or what"])

    def test_two_questions_fails(self):
        problems = self.walk(entry(1, "A", "Who is it for? What will it cost?"))
        self.assertEqual(problems, ["slide 1: Question asks more than one thing"])


class ImportTests(Base):
    def test_import_html_writes_slides_and_notes(self):
        page = self.root / "deck" / "talk.html"
        page.write_text(HTML, encoding="utf-8")
        self.assertIn("already here", importer.import_deck(page))
        self.assertIn("imported 2 slides (1 with notes)", importer.import_deck(page, force=True))
        slides = (self.root / "deck" / "slides.md").read_text(encoding="utf-8")
        self.assertIn("## Slide 1: Cover", slides)
        self.assertIn("## Slide 2: Study 2\nStudy 2 Planted attacks", slides)
        self.assertNotIn("var x", slides)
        self.assertNotIn("welcome", slides)
        self.assertIn("SAY: welcome everyone.", (self.root / "deck" / "notes.md").read_text(encoding="utf-8"))
        self.assertIn("slides: 2", deck.status(self.root))

    def test_page_without_slides_says_so(self):
        page = self.root / "deck" / "plain.html"
        page.write_text("<p>no slides</p>", encoding="utf-8")
        self.assertIn("no slides found", importer.import_deck(page, force=True))


if __name__ == "__main__":
    unittest.main()
