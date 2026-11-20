#!/usr/bin/env python3
"""Turn an HTML slide deck into deck/slides.md and deck/notes.md, so the tutor can read every slide.

    python _tools/import_html.py deck/your-deck.html [--force]

Reads one slide per <section class="slide ...">. The title is the section's data-title, else its first
heading. Speaker notes come from an <aside hidden> inside the section. Writes next to the HTML file and
will not replace an existing slides.md or notes.md unless --force is given. Standard library only.
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP_TAGS = {"script", "style", "svg", "template"}
HEADINGS = {"h1", "h2", "h3"}
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "area", "col", "embed", "track"}


class SlideParser(HTMLParser):
    """Collects (title, text, notes) for each slide section."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slides, self.stack, self.cur = [], [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in VOID:
            return
        role = ""
        if tag == "section" and "slide" in (a.get("class") or "").split():
            self.cur = {"title": a.get("data-title") or "", "text": [], "notes": [], "head": []}
            role = "slide"
        elif self.cur is not None and tag == "aside" and "hidden" in a:
            role = "notes"
        elif tag in SKIP_TAGS:
            role = "skip"
        elif tag in HEADINGS:
            role = "head"
        self.stack.append((tag, role))

    def handle_endtag(self, tag):
        while self.stack:
            t, role = self.stack.pop()
            if role == "slide" and self.cur is not None:
                self.slides.append(self.cur)
                self.cur = None
            if t == tag:
                return

    def handle_data(self, data):
        if self.cur is None or not data.strip():
            return
        roles = {r for _, r in self.stack}
        if "skip" in roles:
            return
        words = " ".join(data.split())
        self.cur["notes" if "notes" in roles else "text"].append(words)
        if "head" in roles and "notes" not in roles:
            self.cur["head"].append(words)


def to_markdown(slides):
    """Return (slides.md text, notes.md text)."""
    deck, notes = ["# Imported deck", ""], ["# Speaker notes", ""]
    for i, s in enumerate(slides, 1):
        title = s["title"] or (s["head"][0] if s["head"] else f"Slide {i}")
        deck += [f"## Slide {i}: {title}", " ".join(s["text"]), ""]
        if s["notes"]:
            notes += [f"## Slide {i}: {title}", " ".join(s["notes"]), ""]
    return "\n".join(deck), "\n".join(notes)


def import_deck(html_path, force=False):
    """Write slides.md and notes.md beside html_path. Return a one-line report."""
    html_path = Path(html_path)
    parser = SlideParser()
    parser.feed(html_path.read_text(encoding="utf-8", errors="replace"))
    if not parser.slides:
        return 'no slides found: expected <section class="slide"> blocks'
    deck_md, notes_md = to_markdown(parser.slides)
    targets = {html_path.parent / "slides.md": deck_md, html_path.parent / "notes.md": notes_md}
    taken = [p.name for p in targets if p.exists()]
    if taken and not force:
        return f"{' and '.join(taken)} already here: add --force to replace"
    for path, text in targets.items():
        path.write_text(text, encoding="utf-8")
    with_notes = sum(1 for s in parser.slides if s["notes"])
    return f"imported {len(parser.slides)} slides ({with_notes} with notes) into {html_path.parent.name}/"


def main(argv):
    args = [a for a in argv[1:] if a != "--force"]
    if len(args) != 1 or not Path(args[0]).is_file():
        print(__doc__)
        return 2
    report = import_deck(args[0], force="--force" in argv)
    print(report)
    return 0 if report.startswith("imported") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
