#!/usr/bin/env python3
"""Check my-work/walkthrough.md against the "never invent a number" rule.

    python _tools/check_walkthrough.py

Prints `pass`, or `fail` followed by one line per problem, and exits 1 on a fail. A slide entry fails
when its "My answer" is empty, or when a number in its "Decided" or "For my project" line is not one
the learner gave: in any "My answer", in my-work/me.md, in a file in my-project/, or as the result of
math shown in the same entry ("... = 2,190"). Standard library only. Run from the workspace root.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRY_HEAD = re.compile(r"^## Slide (\d+)", re.M)
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")
CHECKED_FIELDS = ("Decided", "For my project")
PROJECT_TEXT = {".md", ".txt", ".csv"}


def norm(num):
    """'2,190' and '2190.00' and '2190' all become '2190'."""
    n = num.replace(",", "")
    return n.rstrip("0").rstrip(".") if "." in n else n


def numbers_in(text):
    return {norm(m) for m in NUMBER.findall(text)}


def field(entry, name):
    m = re.search(rf"- \*\*{re.escape(name)}:\*\*[ \t]*(.*)", entry)
    return m.group(1).strip() if m else ""


def entries(text):
    """Split the walkthrough (below its first ---) into (slide number, entry text)."""
    body = text.split("\n---\n", 1)[-1]
    heads = list(ENTRY_HEAD.finditer(body))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        yield int(m.group(1)), body[m.start():end]


def given_numbers(root, entry_list):
    """Every number the learner gave: their answers, me.md and the my-project files."""
    given = set()
    for _, entry in entry_list:
        given |= numbers_in(field(entry, "My answer"))
    me = root / "my-work" / "me.md"
    if me.exists():
        given |= numbers_in(me.read_text(encoding="utf-8"))
    for f in (root / "my-project").rglob("*"):
        if f.is_file() and f.suffix.lower() in PROJECT_TEXT and f.name != "README.md":
            given |= numbers_in(f.read_text(encoding="utf-8", errors="replace"))
    return given


def problems_in(n, entry, given):
    if re.search(r"- \*\*Skipped\*\*", entry):
        return []
    if not field(entry, "My answer"):
        return [f"slide {n}: no answer written"]
    shown = {norm(m) for m in re.findall(r"=\s*\$?(\d[\d,]*(?:\.\d+)?)", entry)}
    found = []
    for name in CHECKED_FIELDS:
        for num in sorted(numbers_in(field(entry, name)) - given - shown):
            found.append(f"slide {n}: {name} has {num}, which the learner never gave")
    return found


def check(root):
    path = root / "my-work" / "walkthrough.md"
    if not path.exists():
        return ["no my-work/walkthrough.md yet: run setup first"]
    entry_list = list(entries(path.read_text(encoding="utf-8")))
    given = given_numbers(root, entry_list)
    problems = []
    for n, entry in entry_list:
        problems += problems_in(n, entry, given)
    return problems


def main():
    problems = check(ROOT)
    if problems:
        print("fail")
        print("\n".join(problems))
        return 1
    print("pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
