#!/usr/bin/env python3
"""Check my-work/walkthrough.md against the "never invent a number" rule.

    python _tools/check_walkthrough.py

Prints `pass`, or `fail` followed by one line per problem, and exits 1 on a fail. A slide entry fails
when its "My answer" is empty, or when a number in its "Decided" or "For my project" line is not one
the learner gave: in any "My answer", in my-work/me.md, in a file in my-project/, or as the result of
math shown in the same entry that adds up ("3 x 730 = 2,190"). Math that does not add up fails. A number on the slide itself (its title or its text in
deck/) also counts as given. It also fails a "Question" line that asks more than one thing (more than
one question mark, or "..., and is it..."), asks for a yes or no ("Do you...", or behind a lead-in:
"If ..., would they...?"; an either/or with "or" is fine), or repeats one of the three questions
before it. Once my-work/summary.md exists it is checked too: every number in it must already be in
the walkthrough, me.md or my-project/, and its "Slides done" line must match the walkthrough.
Standard library only. Run from the workspace root.
"""
import ast
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("deck", Path(__file__).resolve().parent / "deck.py")
deck = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(deck)
ENTRY_HEAD = re.compile(r"^## Slide (\d+)", re.M)
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")
CHECKED_FIELDS = ("Decided", "For my project")
PROJECT_TEXT = {".md", ".txt", ".csv"}
YES_NO = {"am", "is", "are", "was", "were", "do", "does", "did", "can", "could", "will", "would",
          "should", "shall", "have", "has", "had", "may", "might", "must"}
ASK_WORDS = {"how", "what", "which", "who", "whom", "whose", "when", "where", "why"} | YES_NO
_NUM = r"\$?\d[\d,]*(?:\.\d+)?"
EQUATION = re.compile(rf"({_NUM}(?:\s*[x×*+\-/]\s*{_NUM})+)\s*=\s*\$?(\d[\d,]*(?:\.\d+)?)")
DONE_LINE = re.compile(r"- \*\*Slides done:\*\*\s*(\d+)\s*of\s*(\d+)\s*\(skipped:\s*(\d+)\)")


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


def slide_numbers(root, n, entry):
    """Numbers the slide itself carries: the entry's heading and the slide's text in deck/."""
    return numbers_in(entry.splitlines()[0]) | numbers_in(deck.slide_text(root, n))


def question_key(q):
    return " ".join(re.findall(r"[a-z0-9']+", q.lower()))


def shape_problem(q):
    """Return what is wrong with the shape of one question, or ""."""
    words = question_key(q).split()
    joined = any(w == "and" and nxt in ASK_WORDS for w, nxt in zip(words, words[1:]))
    if q.count("?") > 1 or joined:
        return "Question asks more than one thing"
    clauses = re.sub(r"'[^']*'|\"[^\"]*\"", "", q).split(",")
    starts = [question_key(c).split()[:1] for c in clauses]
    lead_in = any(s and s[0] in YES_NO for s in starts[1:]) and " or " not in f" {question_key(q)} "
    if (words and words[0] in YES_NO) or lead_in:
        return "Question is a yes or no question; ask how or what"
    return ""


def question_problems(entry_list):
    """Fail a Question that asks two things, asks for a yes or no, or repeats one of the last three."""
    found, asked = [], []
    for n, entry in entry_list:
        q = field(entry, "Question")
        if not q:
            continue
        words = question_key(q).split()
        if shape_problem(q):
            found.append(f"slide {n}: {shape_problem(q)}")
        if words and question_key(q) in asked[-3:]:
            found.append(f"slide {n}: Question repeats one of the last three")
        asked.append(question_key(q))
    return found


def arithmetic(expr):
    """Work out 'a x b + c' with numbers and + - x * / only; None if it is anything else."""
    text = expr.replace("$", "").replace(",", "").replace("×", "*").replace("x", "*")
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError:
        return None
    if not all(isinstance(n, (ast.Expression, ast.BinOp, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div))
               for n in ast.walk(tree)):
        return None
    try:
        return eval(compile(tree, "<math>", "eval"))  # only numbers and + - * / reach this line
    except ZeroDivisionError:
        return None


def shown_math(entry):
    """Return (results of math that adds up, problems for math that does not)."""
    shown, found = set(), []
    for m in EQUATION.finditer(entry):
        value, said = arithmetic(m.group(1)), float(m.group(2).replace(",", ""))
        if value is not None and abs(value - said) <= max(0.01, 0.005 * abs(value)):
            shown.add(norm(m.group(2)))
        else:
            found.append(f"math does not add up: {' '.join(m.group(0).split())}")
    return shown, found


def problems_in(n, entry, given):
    if re.search(r"- \*\*Skipped\*\*", entry):
        return []
    if not field(entry, "My answer"):
        return [f"slide {n}: no answer written"]
    shown, found = shown_math(entry)
    found = [f"slide {n}: {f}" for f in found]
    for name in CHECKED_FIELDS:
        for num in sorted(numbers_in(field(entry, name)) - given - shown):
            found.append(f"slide {n}: {name} has {num}, which the learner never gave")
    return found


def summary_problems(root, walk_text, given):
    """Summary: no number the walkthrough, me.md or my-project/ lacks; the slide count must match."""
    path = root / "my-work" / "summary.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    done, skipped = deck.walked(root)
    found_deck = deck.find_deck(root)
    total = deck.slide_count(found_deck) if found_deck else 0
    m = DONE_LINE.search(text)
    if not m:
        return ["summary: fill the Slides done line as 'X of Y (skipped: Z)'"]
    found = []
    if tuple(int(g) for g in m.groups()) != (len(done), total, len(skipped)):
        found.append(f"summary: Slides done should say {len(done)} of {total} (skipped: {len(skipped)})")
    allowed = given | numbers_in(walk_text) | {str(i) for i in range(total + 1)}
    for num in sorted(numbers_in(text) - allowed):
        found.append(f"summary: {num} is not in the walkthrough or anything the learner gave")
    return found


def check(root):
    path = root / "my-work" / "walkthrough.md"
    if not path.exists():
        return ["no my-work/walkthrough.md yet: run setup first"]
    walk_text = path.read_text(encoding="utf-8")
    entry_list = list(entries(walk_text))
    given = given_numbers(root, entry_list)
    problems = []
    for n, entry in entry_list:
        problems += problems_in(n, entry, given | slide_numbers(root, n, entry))
    body = walk_text.split("\n---\n", 1)[-1]
    return problems + question_problems(entry_list) + summary_problems(root, body, given)


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
