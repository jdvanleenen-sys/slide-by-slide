# 01_setup: get to know the learner before slide 1

One job: write `my-work/me.md` so every slide can be tied to their real work.

## Inputs
- Working: `deck/` (to count the slides), `my-project/` (whatever they put there)
- Reference: `_shared/coaching-rules.md`, `_templates/me.md`

## Process
1. Greet them in one line: you will go through the deck one slide at a time, using their own project.
2. Ask these five questions **one at a time**, waiting for each answer:
   1. What are you building, working on or teaching? (one or two sentences)
   2. Who is it for: the real person, business or audience you want to help?
   3. What should they be able to do after this that they cannot do now?
   4. What is your next deadline, if you have one?
   5. Anything in `my-project/` I should read first? (If it is empty, they can copy files into the
      `my-project/` folder, or carry on without.)
3. Copy `_templates/me.md`, `_templates/walkthrough.md` and `_templates/later.md` into `my-work/`.
   Fill `me.md` with their answers, in their words. Write "not given" for anything they skipped.
4. Run `python _tools/deck.py status`. If it says the deck is empty, or names an HTML deck to import,
   tell them what it says (copy the deck into the `deck/` folder, or run the import line it prints) and
   stop here.
5. Show them `me.md` in a few lines and ask: "Is that right?"

## Outputs
- `my-work/me.md`, `my-work/walkthrough.md`, `my-work/later.md`

## Check
The learner says `me.md` is right. Then go straight to slide 1 in `02_slides/CONTEXT.md`.
