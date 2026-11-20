# Changes

## v1.2 (2026-11-19): three more loops, two of them driven by cold runs

Each loop: pass or fail checks written first and never edited, 3 attempts at most, only failing parts
changed, every earlier loop's checks rerun as regression checks.

**Loop 2: the gaps left after v1.1** (15 checks)

| Attempt | Pass | What failed | Change carried |
|---|---|---|---|
| 0 | 5 / 15 | D1 to D10 | none: the baseline |
| 1 | 15 / 15 | none | question check catches a yes or no behind a lead-in and two asks joined by "and"; summary number and slide-count check; importer keeps diagram labels and drops screen chrome |

D10 was a cold run: a fresh agent with no memory ran the sample deck from setup to wrap-up against a
scripted learner. Every check passed and nothing outside `my-work/` changed. (D3's label names slides
5, 8 and 9; the real bad questions are slides 5, 7 and 9, which is what the test checks.)

**Loop 3: what the cold run found** (13 checks)

| Attempt | Pass | What failed | Change carried |
|---|---|---|---|
| 0 | 3 / 13 | E1 to E9, E13 | none: the baseline |
| 1 | 9 / 13 | E3 (a line break hid "five short questions"), loop 1's C5 (the step 3 rewrite dropped "suggest" and "decide"), E12, E13 | the questions the steps script are now open questions; setup checks the deck before writing a file; wrap-up asks the next step before filling the summary; a suggested skip is the slide's one question; inline `Notes:` lines show as speaker notes; numbers given mid-deck go into `me.md` |
| 2 | 13 / 13 | none | README line re-wrapped; step 3 keeps "suggest" and "the learner decide" |

Found on the way: a `notes.md` heading with no title (`## Slide 1`, the documented format) swallowed
the first line of the note. Fixed and tested. E13 was a second cold run on the fixed version.

**Loop 4: the shown-math hole** (7 checks)

The second cold run reported that any number written after "=" passed. Tried before fixing:
`Decided: Charge 3 x 4000 = 99000.` passed the check.

| Attempt | Pass | What failed | Change carried |
|---|---|---|---|
| 0 | 3 / 7 | F1, F2, F4, F5 | none: the baseline |
| 1 | 6 / 7 | F2: the new tests never had the learner give the numbers being multiplied | the check now works the math out; math that does not add up fails; coaching rule 3 says to write math in numbers only; root `CONTEXT.md` lists everything the check accepts |
| 2 | 6 / 7 | F7: the README test count was stale | test helper takes the learner's answer |
| 3 | 7 / 7 | none | README test count |

### Known limits after v1.2

- Whether "My answer" and "Decided" are in the learner's own words is not checked by code.
- Math written in words ("6 hours at 60 an hour is 360") cannot be worked out; the result then fails
  as a number the learner never gave, which is safe but noisy.
- No rule yet for a project the learner builds for their own use, where a slide's "them" (the
  customer) and the learner's own numbers differ. That needs a coaching call, not a script.
- A finished run (`summary.md` exists) has no row in `AGENTS.md`, so a new session goes to wrap-up again.
- Running the check commands creates `__pycache__` folders under `_tools/` and `tests/`, which the
  "never change `_tools/`" rule does not allow for. They are git-ignored.

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
