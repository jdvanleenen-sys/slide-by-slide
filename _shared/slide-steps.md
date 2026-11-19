# The six steps every slide follows

The one home for how a slide runs. `02_slides/CONTEXT.md` points here.

1. **Show the slide.** Run `python _tools/deck.py show N`. For a PDF deck it writes the slide as a
   picture to `my-work/slides/slide-N.png` and prints the path: point the learner at that file so they
   can look at it while they answer. For a `slides.md` deck it prints the slide's text: quote it.
   If the picture cannot be made, tell the learner to open slide N of the deck themselves.
2. **Say what is being taught,** in two or three plain sentences. Use the speaker notes if the deck has
   them. Do not add points the slide does not make.
3. **Say what it means for their project,** using their real customer and their real numbers from
   `my-work/me.md` and `my-project/`. If the slide does not fit their project, say so plainly.
4. **Ask one question about their real work.** Then stop and wait.
5. **Write it down.** Once they answer, add the slide's entry to `my-work/walkthrough.md` in the shape
   `_templates/walkthrough.md` shows: their answer in their words, what was decided, any follow-up.
   Then run `python _tools/check_walkthrough.py`. If it prints `fail`, fix the entry (usually a number
   they never said) before you go on.
6. **Wait for "next".** Only "next" moves to slide N+1. A pushback round on the same slide is fine.
