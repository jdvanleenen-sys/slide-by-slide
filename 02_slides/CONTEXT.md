# 02_slides: one slide, one question, then wait

One job: teach the next slide against the learner's real work and write down what they decide.

## Inputs
- Working: `my-work/me.md`, `my-work/walkthrough.md`, `my-project/`, slide N of `deck/`
- Reference: `_shared/coaching-rules.md`, `_shared/slide-steps.md`, `_templates/walkthrough.md`

Do NOT load: the whole deck at once, other slides' pictures, `03_wrap-up/`.

## Process
1. Run `python _tools/deck.py status` to find N, the next slide.
2. Follow the six steps in `_shared/slide-steps.md` for slide N.
3. On "next", go back to 1. On "skip", write a skipped entry and go back to 1.
4. When `deck.py status` says no slides are left, or the learner says "wrap up", go to
   `03_wrap-up/CONTEXT.md`.

## Outputs
- One entry per slide in `my-work/walkthrough.md`
- Lines in `my-work/later.md` for anything that belongs somewhere else

## Check
`python _tools/check_walkthrough.py` prints `pass` after every entry. A `fail` is fixed before "next".
