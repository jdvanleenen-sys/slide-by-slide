# deck: the slides being learned

Put one deck here: a PDF (one slide per page), or `slides.md` with each slide under `## Slide N: title`
and an optional `Notes:` line. Speaker notes as a separate file: name it `notes.md`, one `## Slide N`
heading per slide. If both a PDF and `slides.md` are here, the PDF is used.

**Use a PDF exported from the deck tool** (PowerPoint, Keynote, Google Slides: File, then Export or
Download as PDF). A PDF made from screenshots holds pictures only, so the tutor cannot read the slide
text and teaches from the picture alone.

**An HTML deck** (one `<section class="slide">` per slide, notes in `<aside hidden>`): copy it here and
run `python _tools/import_html.py deck/your-deck.html`. It writes `slides.md` and `notes.md` next to it.
Add `--force` to replace the sample `slides.md`.

The sample `slides.md` lets the workspace run on first open. Replace it with your course deck.
