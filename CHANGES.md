# Changes

## v1.1 (2026-11-19): the seven fixes from the first real-deck run

Found by walking a real 15-slide deck (an AI security talk) as a teacher getting it ready for staff.

| # | Found | Fix |
|---|---|---|
| 1 | The slide should be on screen before any teaching | Step 1 runs `deck.py show N --open`, which opens the picture first |
| 2 | "Study 2" in a slide title failed the number check | A number on the slide itself (title or text) counts as given |
| 3 | Setup asked for a deadline and files, which does not fit a teacher | New setup question: what should they be able to do after this? |
| 4 | Four slides did not fit the learner | The tutor suggests a skip; only the learner says "skip" |
| 5 | Slide 9 asked what slide 2 asked | The tutor reads the last three questions first; the check fails a repeat |
| 6 | A question had two parts, one a yes or no | Coaching rule 2: one question mark, start with How or What; the check fails a yes or no opener |
| 7 | A deck saved as pictures has no text | `deck.py` says so; `deck/README.md` asks for an exported PDF; new `_tools/import_html.py` for HTML decks |
| + | Setup and deck text pointed at a platform upload button | Now "copy into the `deck/` folder": it runs on the learner's computer |
| + | `links.py` had a 78-line function | Split into small parts; output checked byte for byte the same |

### How it was checked: a refinement loop, 3 attempts max

16 pass or fail checks, written before any change and never edited after (`C1` to `C16`: one per fix,
plus all tests pass, links resolve, no em dash, files under 300 lines and functions under 50).

| Attempt | Pass | What failed | Change carried |
|---|---|---|---|
| 0 (before) | 3 / 16 | C1 to C12, C16 | none: the baseline |
| 1 | 15 / 16 | C6: "last" and "three" split across a line break in step 4 | all fixes made |
| 2 | 16 / 16 | none | only the step 4 line re-wrapped |

Then a run on real input: the 15-slide HTML deck imported (15 slides, 15 with notes), "Study 2" passed
the number check, and the question check caught the yes or no question on slide 9.

### Known limits (not counted, so not caught)

- A yes or no question behind a lead-in ("If a supplier's PDF said..., would your staff notice?").
- Two questions joined by "and" under one question mark.
- Whether a question is a good one. That is the learner's and the coach's read, not a script's.
