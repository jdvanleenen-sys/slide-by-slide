# Slide by Slide

*Agents: start at `AGENTS.md`. This page is for people.*

Learn a slide deck by using it on your own work. Open the workspace and the tutor asks you
five short questions about what you are building. Then it takes you through the deck one slide at a time: it shows
the slide, says what it teaches in plain words, ties it to your project, asks you one question and
writes your answer down. You say "next" when you are ready for the next slide.

At the end you have a walkthrough of every answer and decision, a Later list, and a one-page summary.

## Use it
1. Put your deck in `deck/` (a PDF, or `slides.md`). A three-slide sample is there so it runs on first open.
2. Put anything about your project in `my-project/`. Leave out anything private.
3. Start a chat. Say "next" to move on, "skip" to skip a slide, "wrap up" to finish early.

## The rules it keeps
One question at a time. It never makes up a number: a script checks every number it writes down
against what you said (`python _tools/check_walkthrough.py`). It changes nothing outside `my-work/`.

## Test it
`python -m unittest discover -s tests` (39 tests, including a planted made-up number the check must catch).

Built by Jeff Van Leenen (AI the vL Way), from Ari Leavesley's coaching brief.
