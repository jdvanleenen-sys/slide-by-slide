# Why it is built this way

The decisions behind this workspace, so a fresh AI or a new builder keeps to them.

1. **The learner learns by answering, not by reading.** A summary of a deck is forgotten by the next
   day. One question about their own work makes them think. That is why there is one question per slide
   and the tutor waits.
2. **Every slide lands on real work.** The deck is the same for everyone; the project is not. Tying each
   slide to the learner's own customer and numbers turns a lecture into decisions they can use the same
   week.
3. **The slide is on screen while they answer.** The teacher's point and the learner's decision sit side
   by side. That is why `deck.py show` makes a picture of a PDF slide.
4. **No made-up numbers, checked by code.** An AI that invents a price teaches the learner nothing and
   can mislead them. The rule is in `_shared/coaching-rules.md`, and `check_walkthrough.py` enforces it,
   because a rule held only by a sentence fails the day the AI forgets it.
5. **Only "next" moves on.** The learner sets the pace. A slide can take one answer or three rounds of
   pushback.
6. **Everything is written down as it happens.** The walkthrough is the learner's record and the
   teacher's view of their thinking. Nothing is lost between sittings.
7. **Nothing outside `my-work/` changes.** The deck and the learner's project are inputs, never edited.
   Ideas that belong elsewhere go to `later.md`.

Where it came from: Ari Leavesley's "Implement with me. Teach me what is happening." coaching brief and
Jeff Van Leenen's slide-by-slide walkthrough of a Lyceum deck (Nov 8 to 10, 2026: 37 slides, every
answer in his own words). Built for the See It, Build It, Own It school by AI the vL Way.
