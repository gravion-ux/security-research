#!/usr/bin/env python3
"""Sanity checks for this docs-only repository.

Fails if any Markdown file is empty, lacks a top-level heading, or links
to a local file that does not exist.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

problems = []
for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts:
        continue
    text = md.read_text(encoding="utf-8")
    rel = md.relative_to(ROOT)
    if not text.strip():
        problems.append(f"{rel}: empty file")
        continue
    if ".github" not in md.parts and not re.search(r"^#\s+\S", text, re.M):
        problems.append(f"{rel}: no top-level heading")
    for target in LINK.findall(text):
        target = target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        if not (md.parent / target).exists():
            problems.append(f"{rel}: broken local link -> {target}")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print("docs ok")
