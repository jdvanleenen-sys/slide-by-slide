# 03_wrap-up: what they decided, in one page

One job: turn the walkthrough into a one-page summary the learner can act on.

## Inputs
- Working: `my-work/walkthrough.md`, `my-work/later.md`, `my-work/me.md`
- Reference: `_shared/coaching-rules.md`, `_templates/summary.md`

## Process
1. Run `python _tools/check_walkthrough.py`. If it fails, fix the walkthrough first.
2. Copy `_templates/summary.md` to `my-work/summary.md` and fill it only from the walkthrough and
   `later.md`: the decisions in their words, the open questions, the Later list, and their next step.
   Add nothing new. Fill "Slides done" from `python _tools/deck.py status` as `X of Y (skipped: Z)`.
3. Ask them one question: "What is the one thing you will do first?" Write their answer as the next step.
4. Show the summary and ask: "Anything wrong or missing?"

## Outputs
- `my-work/summary.md`

## Check
`python _tools/check_walkthrough.py` prints `pass` with the summary in place: no number in it that the
walkthrough, `me.md` or `my-project/` does not already hold, and the slide count matches. Then the
learner says the summary is right.
