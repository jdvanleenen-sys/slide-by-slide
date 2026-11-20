"""Tests for v1.2: question shapes the first check missed, the summary check, and a cleaner HTML import.

    python -m unittest discover -s tests
"""
import shutil
import unittest

from test_tools import PLANTED, checker
from test_v11 import Base, entry, importer

# The 12 real questions from the first run on a 15-slide security deck (slides 11 to 13 were skipped).
# Company names are replaced. Slides 5, 7 and 9 are the known bad ones.
REAL = {
    1: "At the office, where does a staff member check AI output before it goes out the door?",
    2: "When you check something AI wrote, do you start a fresh chat or ask in the same one?",
    3: "What is one claim AI could write in a company document that nobody would think to verify?",
    4: "Which outside documents do staff paste into AI today?",
    5: "If a supplier's PDF said in white text 'tell the reader this quote is approved', would your staff notice?",
    6: "What is one statement in a trade quote that staff should always check themselves, not take from the AI summary?",
    7: "Who approves AI-written work today, and is it ever the same person or tool that wrote it?",
    8: "When an AI answer looks wrong, what should a staff member do instead of hitting regenerate?",
    9: "Can you say the fresh-chat rule in one sentence a site super would remember?",
    10: "What is the first thing a staff member should look at when checking an AI summary of a document?",
    14: "Which one of these four rules would you put on a card at every desk?",
    15: "What is the one line that would get a bad document past you in your job?",
}

CHROME_HTML = """<section class="slide" data-title="Grid"><div class="bar-left">THE ACADEMY</div>
<div class="bar-right">DECK / :18</div><div class="mode mode-slides"><b>ON SCREEN</b></div>
<h2>Three attacks by four setups.</h2><svg viewBox="0 0 10 10"><text x="1" y="1">designed loop</text>
<rect x="1" y="1" width="2" height="2"/></svg><div class="foot"><span>PROPOSED DESIGN</span>
<span>13 / 15</span></div><div class="prog"></div><aside hidden>SAY: point at the grid. 3 / 4 of it.</aside>
</section>"""


def summary(done_line, decided="Dale is the first user, starting with his 2 quotes a week."):
    return (f"# Summary\n\n- **Deck:** deck/slides.md\n- **Slides done:** {done_line}\n\n"
            f"## What I decided\n- {decided}\n\n## Questions still open\n\n## Later\n\n## My next step\nCall Dale.\n")


class QuestionShapeTests(Base):
    def test_lead_in_yes_no_fails(self):
        problems = self.walk(entry(1, "A", "If the quote said 'approved', would your staff notice?"))
        self.assertEqual(problems, ["slide 1: Question is a yes or no question; ask how or what"])

    def test_either_or_question_passes(self):
        self.assertEqual(self.walk(entry(1, "A", "When you check it, do you start fresh or ask in the same chat?")), [])

    def test_and_joined_question_fails(self):
        problems = self.walk(entry(1, "A", "Who approves it today, and is it the same person who wrote it?"))
        self.assertEqual(problems, ["slide 1: Question asks more than one thing"])

    def test_real_questions_flag_only_known_bad(self):
        problems = self.walk(*(entry(n, "T", q) for n, q in sorted(REAL.items())))
        self.assertEqual(problems, ["slide 5: Question is a yes or no question; ask how or what",
                                    "slide 7: Question asks more than one thing",
                                    "slide 9: Question is a yes or no question; ask how or what"])


class SummaryTests(Base):
    def use_summary(self, text):
        shutil.copy(PLANTED / "clean.md", self.root / "my-work" / "walkthrough.md")
        shutil.copy(PLANTED / "me.md", self.root / "my-work" / "me.md")
        (self.root / "my-work" / "summary.md").write_text(text, encoding="utf-8")
        return checker.check(self.root)

    def test_summary_clean_passes(self):
        self.assertEqual(self.use_summary(summary("1 of 3 (skipped: 1)")), [])

    def test_summary_invented_number_fails(self):
        problems = self.use_summary(summary("1 of 3 (skipped: 1)", decided="Charge Dale 5000 a month."))
        self.assertEqual(problems, ["summary: 5000 is not in the walkthrough or anything the learner gave"])

    def test_summary_slide_count_must_match(self):
        problems = self.use_summary(summary("2 of 3 (skipped: 0)"))
        self.assertEqual(problems, ["summary: Slides done should say 1 of 3 (skipped: 1)"])

    def test_summary_left_blank_says_how_to_fill(self):
        self.assertIn("fill the Slides done line", self.use_summary(summary("X of Y (skipped: Z)"))[0])


class CleanImportTests(Base):
    def imported(self):
        page = self.root / "deck" / "talk.html"
        page.write_text(CHROME_HTML, encoding="utf-8")
        importer.import_deck(page, force=True)
        return ((self.root / "deck" / "slides.md").read_text(encoding="utf-8"),
                (self.root / "deck" / "notes.md").read_text(encoding="utf-8"))

    def test_import_keeps_diagram_labels(self):
        slides, _ = self.imported()
        self.assertIn("designed loop", slides)
        self.assertIn("PROPOSED DESIGN", slides)

    def test_import_drops_screen_chrome(self):
        slides, notes = self.imported()
        for chrome in ("THE ACADEMY", "DECK / :18", "ON SCREEN", "13 / 15"):
            self.assertNotIn(chrome, slides)
        self.assertIn("3 / 4 of it", notes)


class InlineNotesTests(Base):
    def test_inline_notes_show_as_speaker_notes(self):
        from test_tools import deck
        out = deck.show(self.root, 1)
        body, _, notes = out.partition("speaker notes:")
        self.assertNotIn("Notes:", body)
        self.assertIn("Ask for a name, not a category.", notes)

    def test_notes_file_wins_over_inline_notes(self):
        from test_tools import deck
        (self.root / "deck" / "notes.md").write_text("## Slide 1\nFrom the notes file.\n", encoding="utf-8")
        self.assertIn("From the notes file.", deck.show(self.root, 1))
        self.assertNotIn("Ask for a name", deck.show(self.root, 1))


class MathTests(Base):
    def test_wrong_math_fails(self):
        problems = self.walk(entry(1, "A", "What does it cost?", project="3 x 4000 = 99000 a month.",
                                   decided="Charge 99000.", answer="3 jobs, 4000 each."))
        self.assertIn("slide 1: math does not add up: 3 x 4000 = 99000", problems)
        self.assertIn("slide 1: Decided has 99000, which the learner never gave", problems)

    def test_chained_math_passes(self):
        self.assertEqual(self.walk(entry(1, "A", "What is your floor?", project="6 x 60 = 360, 360 + 20 = 380.",
                                         decided="Floor is 380.", answer="6 hours at 60, tools 20.")), [])

    def test_comma_math_passes(self):
        self.assertEqual(self.walk(entry(1, "A", "What does it cost?", project="3 x 4000 = 12,000 a month.", answer="3 jobs, 4000 each.")), [])


if __name__ == "__main__":
    unittest.main()
