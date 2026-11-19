# How a run goes: setup, then the slides, then the wrap-up

One run is one learner working through one deck. It can take several sittings; every sitting starts by
reading where they are from `my-work/`.

| Step | Folder | Reads | Writes | Ends when |
|---|---|---|---|---|
| 1 | `01_setup/` | `deck/`, `my-project/` | `my-work/me.md`, the blank `walkthrough.md` and `later.md` | the learner confirms `me.md` |
| 2 | `02_slides/` | `me.md`, the slide, `my-project/` | one entry per slide in `walkthrough.md`; lines in `later.md` | the last slide, or "wrap up" |
| 3 | `03_wrap-up/` | `walkthrough.md`, `later.md` | `my-work/summary.md` | the learner confirms the summary |

## Status, read from disk

- No `my-work/me.md`: setup has not run.
- `python _tools/deck.py status` prints the slide count, the slides done or skipped, and the next slide.
- `my-work/summary.md` exists: the run is finished.

## The one check that is a script

`python _tools/check_walkthrough.py` reads `my-work/walkthrough.md` and `my-work/me.md`. It fails when a
slide entry has no answer, or when a number in "Decided" or "For my project" appears nowhere in the
learner's own answers or in `me.md`. That is the "never invent a number" rule, checked by code.
`python -m unittest discover -s tests` proves it catches a planted invented number.
