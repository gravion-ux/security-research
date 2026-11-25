"""Make the repository's validator importable from the test suite.

The validator lives in `scripts/`, which is not a package, so its directory is
added to `sys.path` here.  This is the same arrangement the other Python
repositories in this account use to keep a flat layout importable without an
install step.
"""
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parent / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
