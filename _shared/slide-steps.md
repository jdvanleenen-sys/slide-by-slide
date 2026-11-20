# The six steps every slide follows

The one home for how a slide runs. `02_slides/CONTEXT.md` points here.

1. **Show the slide first, before you say anything about it.** Run `python _tools/deck.py show N --open`.
   For a PDF deck it writes the slide as a picture to `my-work/slides/slide-N.png`, opens it on the
   learner's screen and prints the path, so they can look at it while they answer. For a `slides.md`
   deck it prints the slide's text: quote it. If the picture cannot be made or opened, give the learner
   the path, or tell them to open slide N of the deck themselves. If it says the slide has no text, the
   deck was saved as pictures: teach from the picture and the notes, and tell the learner once that a
   PDF exported from the deck tool works better.
2. **Say what is being taught,** in two or three plain sentences. Use the speaker notes if the deck has
   them. Do not add points the slide does not make.
3. **Say what it means for their project,** using their real customer and their real numbers from
   `my-work/me.md` and `my-project/`. If the slide does not fit their project, say so plainly,
   suggest skipping it, and let the learner decide. Only they say "skip".
4. **Ask one question about their real work.** Before you ask, read the **Question** lines of the
   last three entries in `my-work/walkthrough.md`, and do not ask the same thing again. Follow coaching rule 2
   for the shape of the question. Then stop and wait.
5. **Write it down.** Once they answer, add the slide's entry to `my-work/walkthrough.md` in the shape
   `_templates/walkthrough.md` shows: their answer in their words, what was decided, any follow-up.
   Then run `python _tools/check_walkthrough.py`. If it prints `fail`, fix the entry (usually a number
   they never said) before you go on.
6. **Wait for "next".** Only "next" moves to slide N+1. A pushback round on the same slide is fine.
