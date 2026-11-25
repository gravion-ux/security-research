"""Tests for the advisory validator.

The validator is the repository's only executable code, so it is tested like
any other code: the checks are exercised against the real advisories, and each
check is also exercised against a deliberately broken document so that a check
which cannot fail is caught.

A validator that silently passes everything would let a malformed advisory be
published, which is the one failure mode this repository cannot afford.
"""
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "scripts"))

import validate_advisories as validator  # noqa: E402

GOOD_ADVISORY = """# Example <= 1.0 — Stored XSS (CWE-79)

| Field | Detail |
| --- | --- |
| Product | Example |
| Affected versions | <= 1.0 |
| Vulnerability | Stored Cross-Site Scripting (CWE-79) |
| Severity | Medium - CVSS 3.1 5.4 |
| Disclosed | 1 Jan 2026, privately to the vendor by email |

## Summary

A description of the defect.

## Impact

What an attacker gains.

## Reproduction

How to reproduce it in a lab.

## Remediation

How to fix it.

## Notes

What was checked before disclosure.
"""


def write(root, name, text):
    path = root / name
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


@pytest.fixture
def advisory_root(tmp_path):
    """A miniature repository holding one valid advisory and a README."""
    write(tmp_path, "example-1.0-stored-xss.md", GOOD_ADVISORY)
    write(tmp_path, "README.md", "# Research\n\n"
         "| # | Product | Vulnerability | Affected | Severity | Status |\n"
         "| --- | --- | --- | --- | --- | --- |\n"
         "| 1 | [Example](example-1.0-stored-xss.md) | Stored XSS | <= 1.0 | Medium | Disclosed |\n")
    return tmp_path


def test_the_repository_has_advisories():
    advisories = validator.advisory_files()
    assert advisories, "the repository ships no advisory documents"


def test_every_advisory_in_this_repository_passes_its_own_checks():
    for advisory in validator.advisory_files():
        assert validator.check_advisory(advisory) == [], advisory.name


def test_every_advisory_in_this_repository_is_linked_from_the_readme():
    problems = validator.check_readme(validator.advisory_files())
    assert problems == []


def test_the_readme_links_all_resolve():
    problems = validator.check_readme(validator.advisory_files())
    assert not any("does not exist" in p for p in problems)


def test_the_tracked_text_files_are_utf8_with_lf_endings():
    assert validator.check_encoding() == []


def test_a_valid_advisory_reports_no_problems(advisory_root):
    advisories = validator.advisory_files(advisory_root)
    assert len(advisories) == 1
    assert validator.check_advisory(advisories[0]) == []


def test_a_missing_summary_row_is_reported(advisory_root):
    advisory = advisory_root / "example-1.0-stored-xss.md"
    advisory.write_text(
        GOOD_ADVISORY.replace("| Severity | Medium - CVSS 3.1 5.4 |\n", ""),
        encoding="utf-8", newline="\n")
    problems = validator.check_advisory(advisory)
    assert any("Severity" in p for p in problems)


def test_a_missing_section_is_reported(advisory_root):
    advisory = advisory_root / "example-1.0-stored-xss.md"
    advisory.write_text(
        GOOD_ADVISORY.replace("## Remediation", "## Workaround"),
        encoding="utf-8", newline="\n")
    problems = validator.check_advisory(advisory)
    assert any("Remediation" in p for p in problems)


def test_a_drafting_marker_is_reported(advisory_root):
    advisory = advisory_root / "example-1.0-stored-xss.md"
    advisory.write_text(
        GOOD_ADVISORY + "\n" + "TO" + "DO: fill in the impact section\n",
        encoding="utf-8", newline="\n")
    problems = validator.check_advisory(advisory)
    assert any("drafting marker" in p for p in problems)


def test_a_missing_title_is_reported(advisory_root):
    advisory = advisory_root / "example-1.0-stored-xss.md"
    advisory.write_text(
        GOOD_ADVISORY.replace("# Example", "Example"),
        encoding="utf-8", newline="\n")
    problems = validator.check_advisory(advisory)
    assert any("title line" in p for p in problems)


def test_an_unlinked_advisory_is_reported(advisory_root):
    write(advisory_root, "second-2.0-stored-xss.md", GOOD_ADVISORY)
    problems = validator.check_readme(validator.advisory_files(advisory_root), advisory_root)
    assert any("second-2.0-stored-xss.md" in p for p in problems)


def test_a_broken_readme_link_is_reported(advisory_root):
    readme = advisory_root / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            "(example-1.0-stored-xss.md)", "(missing-advisory.md)"),
        encoding="utf-8", newline="\n")
    problems = validator.check_readme(validator.advisory_files(advisory_root), advisory_root)
    assert any("does not exist" in p for p in problems)


def test_crlf_line_endings_are_reported(advisory_root):
    advisory = advisory_root / "example-1.0-stored-xss.md"
    advisory.write_bytes(GOOD_ADVISORY.replace("\n", "\r\n").encode("utf-8"))
    problems = validator.check_encoding(advisory_root)
    assert any("CRLF" in p for p in problems)


def test_a_missing_final_newline_is_reported(advisory_root):
    advisory = advisory_root / "example-1.0-stored-xss.md"
    advisory.write_bytes(GOOD_ADVISORY.rstrip("\n").encode("utf-8"))
    problems = validator.check_encoding(advisory_root)
    assert any("does not end with a newline" in p for p in problems)
