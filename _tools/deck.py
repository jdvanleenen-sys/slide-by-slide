#!/usr/bin/env python3
"""Find the deck, say where the learner stands, and show one slide.

    python _tools/deck.py status            slide count, slides done or skipped, the next slide
    python _tools/deck.py show N            slide N: its text, its notes, and for a PDF a picture
    python _tools/deck.py show N --open     the same, and opens the picture on the learner's screen

Run from the workspace root. Standard library, plus PyMuPDF for PDF pictures when it is installed.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLIDE_HEAD = re.compile(r"^## Slide (\d+):?\s*(.*)$", re.M)
PDF_PAGE = re.compile(rb"/Type\s*/Page(?![s\w])")
ZOOM = 1.5
EMPTY = "deck: empty. Copy the slides into the deck/ folder (a PDF, or slides.md)."
NO_TEXT = "(none: this slide has no text, the deck was saved as pictures)"


def find_deck(root):
    """Return the deck file: the first PDF in deck/, else deck/slides.md, else None."""
    pdfs = sorted((root / "deck").glob("*.pdf"))
    if pdfs:
        return pdfs[0]
    md = root / "deck" / "slides.md"
    return md if md.exists() else None


def html_hint(root):
    """Tell the learner how to import an HTML deck, if that is all deck/ holds."""
    pages = sorted((root / "deck").glob("*.htm*"))
    if not pages:
        return EMPTY
    name = pages[0].relative_to(root).as_posix()
    return f"deck: {name} is an HTML deck. Run: python _tools/import_html.py {name}"


def md_slides(path):
    """Map slide number to (title, body) for a slides.md deck."""
    text = path.read_text(encoding="utf-8")
    heads = list(SLIDE_HEAD.finditer(text))
    slides = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        slides[int(m.group(1))] = (m.group(2).strip(), text[m.end():end].strip())
    return slides


def slide_count(deck):
    if deck.suffix.lower() == ".md":
        return len(md_slides(deck))
    try:
        import pymupdf
        with pymupdf.open(deck) as doc:
            return doc.page_count
    except ImportError:
        return len(PDF_PAGE.findall(deck.read_bytes()))


def slide_text(root, n):
    """The words on slide n (title and body), or "" when they cannot be read."""
    deck = find_deck(root)
    if deck is None:
        return ""
    if deck.suffix.lower() == ".md":
        title, body = md_slides(deck).get(n, ("", ""))
        return f"{title}\n{body}"
    try:
        import pymupdf
        with pymupdf.open(deck) as doc:
            return doc[n - 1].get_text() if 1 <= n <= doc.page_count else ""
    except ImportError:
        return ""


def walked(root):
    """Return (done, skipped): slide numbers already in my-work/walkthrough.md."""
    path = root / "my-work" / "walkthrough.md"
    if not path.exists():
        return set(), set()
    text = path.read_text(encoding="utf-8").split("\n---\n", 1)[-1]
    done, skipped = set(), set()
    for m in SLIDE_HEAD.finditer(text):
        n = int(m.group(1))
        nxt = text[m.end():m.end() + 200]
        (skipped if re.match(r"\s*- \*\*Skipped\*\*", nxt) else done).add(n)
    return done, skipped


def status(root):
    deck = find_deck(root)
    if deck is None:
        return html_hint(root)
    total = slide_count(deck)
    done, skipped = walked(root)
    left = [n for n in range(1, total + 1) if n not in done | skipped]
    nxt = left[0] if left else "none left: go to 03_wrap-up"
    return (f"deck: {deck.relative_to(root).as_posix()} | slides: {total} | done: {len(done)} | "
            f"skipped: {len(skipped)} | next: {nxt}")


def notes_for(root, n):
    path = root / "deck" / "notes.md"
    if not path.exists():
        return ""
    return md_slides(path).get(n, ("", ""))[1]


def open_file(path):
    """Open a file with the computer's own viewer."""
    if sys.platform.startswith("win"):
        os.startfile(path)
    else:
        subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", str(path)])


def show_pdf(root, deck, n):
    """Return (text to print, picture path or None) for slide n of a PDF deck."""
    try:
        import pymupdf
    except ImportError:
        return f"No picture tool here. Ask the learner to open slide {n} of {deck.name} themselves.", None
    with pymupdf.open(deck) as doc:
        if not 1 <= n <= doc.page_count:
            return f"There is no slide {n}; the deck has {doc.page_count}.", None
        page = doc[n - 1]
        out = root / "my-work" / "slides" / f"slide-{n}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        page.get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM)).save(out)
        text = page.get_text().strip() or NO_TEXT
    return f"picture: {out.relative_to(root).as_posix()}\ntext on the slide:\n{text}", out


def show(root, n, opener=None):
    """Slide n as text; with an opener, a PDF slide's picture is also opened on screen."""
    deck = find_deck(root)
    if deck is None:
        return html_hint(root)
    picture = None
    if deck.suffix.lower() == ".md":
        slides = md_slides(deck)
        if n not in slides:
            return f"There is no slide {n}; the deck has {len(slides)}."
        title, body = slides[n]
        out = f"Slide {n}: {title}\n{body}"
    else:
        out, picture = show_pdf(root, deck, n)
    if opener and picture:
        try:
            opener(picture)
            out += "\nopened on screen"
        except OSError as err:
            out += f"\ncould not open it ({err}): give the learner the path"
    notes = notes_for(root, n)
    return out + (f"\nspeaker notes:\n{notes}" if notes else "")


def main(argv):
    if len(argv) >= 2 and argv[1] == "status":
        print(status(ROOT))
        return 0
    wants_open = argv[3:] == ["--open"]
    if len(argv) in (3, 4) and argv[1] == "show" and argv[2].isdigit() and (len(argv) == 3 or wants_open):
        print(show(ROOT, int(argv[2]), open_file if wants_open else None))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
