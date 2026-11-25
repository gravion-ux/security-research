"""Validate the advisory documents in this repository.

This repository is Markdown only, so the repository's test suite is this
script.  It checks the structural contract that every advisory in here is
expected to meet, so a draft that is published with a missing section or a
leftover drafting marker fails CI rather than reaching a reader.

The checks are:

  1. every advisory has a title line;
  2. every advisory has a summary table with the required rows;
  3. every advisory has the required sections;
  4. no advisory carries a leftover drafting marker;
  5. every advisory is linked from the README, and every README link resolves;
  6. every tracked text file is UTF-8, uses LF line endings, and ends with a
     newline.

Run it directly:

    python scripts/validate_advisories.py

It exits 0 when every check passes and 1 otherwise, printing one line per
problem.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Files at the repository root that are not advisories.
NON_ADVISORY = {
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
}

REQUIRED_FIELDS = [
    "Product",
    "Affected versions",
    "Vulnerability",
    "Severity",
    "Disclosed",
]

REQUIRED_SECTIONS = [
    "Summary",
    "Impact",
    "Reproduction",
    "Remediation",
    "Notes",
]

# The drafting markers are assembled from fragments so that this file does not
# itself contain the literal strings it looks for.
MARKERS = ["TO" + "DO", "FIX" + "ME", "TB" + "D", "XX" + "X", "PLACE" + "HOLDER"]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def advisory_files():
    return sorted(
        path for path in ROOT.glob("*.md")
        if path.name not in NON_ADVISORY and not path.name.startswith(".")
    )


def check_advisory(path):
    problems = []
    text = path.read_text(encoding="utf-8")

    if not text.startswith("# "):
        problems.append("%s: does not start with a title line" % path.name)

    for field in REQUIRED_FIELDS:
        if not re.search(r"^\|\s*%s\s*\|" % re.escape(field), text, re.MULTILINE):
            problems.append("%s: the summary table has no %r row" % (path.name, field))

    headings = re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    for section in REQUIRED_SECTIONS:
        if not any(h.strip().lower().startswith(section.lower()) for h in headings):
            problems.append("%s: missing the %r section" % (path.name, section))

    for marker in MARKERS:
        if marker in text:
            problems.append("%s: contains the drafting marker %r" % (path.name, marker))

    return problems


def check_readme(advisories):
    problems = []
    readme = ROOT / "README.md"
    if not readme.exists():
        return ["README.md is missing"]
    text = readme.read_text(encoding="utf-8")

    linked = set()
    for target in LINK_RE.findall(text):
        target = target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        linked.add(target)
        if not (ROOT / target).exists():
            problems.append("README.md links to %s, which does not exist" % target)

    for advisory in advisories:
        if advisory.name not in linked:
            problems.append("README.md does not link to %s" % advisory.name)

    for marker in MARKERS:
        if marker in text:
            problems.append("README.md contains the drafting marker %r" % marker)

    return problems


def blob_bytes(path):
    """The bytes git would store for this path, or the working-tree bytes.

    A working tree on Windows with `core.autocrlf=true` holds CRLF while the
    blob holds LF, so checking the working tree would report a problem for a
    file that is published correctly.  The indexed blob is what is published,
    so that is what is checked.
    """
    relative = path.relative_to(ROOT).as_posix()
    try:
        proc = subprocess.run(
            ["git", "-C", str(ROOT), "show", ":" + relative],
            capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return path.read_bytes()
    if proc.returncode == 0:
        return proc.stdout
    return path.read_bytes()


def check_encoding():
    problems = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        parts = set(path.parts)
        if ".git" in parts or "node_modules" in parts:
            continue
        if path.suffix not in (".md", ".py", ".yml", ".yaml", ".txt"):
            continue
        raw = blob_bytes(path)
        if b"\r\n" in raw:
            problems.append("%s: contains CRLF line endings" % path.relative_to(ROOT))
        if raw and not raw.endswith(b"\n"):
            problems.append("%s: does not end with a newline" % path.relative_to(ROOT))
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError:
            problems.append("%s: is not valid UTF-8" % path.relative_to(ROOT))
    return problems


def main():
    advisories = advisory_files()
    if not advisories:
        print("FAIL: no advisory documents found")
        return 1

    problems = []
    for advisory in advisories:
        problems.extend(check_advisory(advisory))
    problems.extend(check_readme(advisories))
    problems.extend(check_encoding())

    if problems:
        print("FAIL: %d problem(s)" % len(problems))
        for problem in problems:
            print("  - %s" % problem)
        return 1

    print("OK: %d advisory document(s) validated" % len(advisories))
    for advisory in advisories:
        print("  - %s" % advisory.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
