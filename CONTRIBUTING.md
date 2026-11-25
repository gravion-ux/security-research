# Contributing to security-research

Thanks for your interest in contributing! `security-research` holds sanitised
advisories for vulnerabilities found in local-lab testing and disclosed to the
affected vendor first.

This document explains how to propose a change and what is expected of an
advisory before it is merged.

## Getting started

1. Fork the repository and clone your fork:

   ```bash
   git clone https://github.com/<your-username>/security-research.git
   cd security-research
   ```

2. Create a branch for your change:

   ```bash
   git checkout -b my-change
   ```

There is no application to install and no test framework to set up — the
repository is Markdown. What you do run is the validator:

```bash
python scripts/validate_advisories.py
```

CI runs the same script on every push and pull request, so a green local run
means the CI check will be green too.

## What an advisory must contain

Every advisory is a Markdown file at the repository root, named
`<product>-<version>-<vulnerability>.md`. The validator checks that it has:

- a title line naming the product and the affected versions;
- a summary table with **Product**, **Affected versions**, **Vulnerability**,
  **Severity** and **Disclosed** rows;
- the sections **Summary**, **Impact**, **Reproduction**, **Remediation** and
  **Notes**;
- no leftover drafting markers.

## Ground rules

- **Local lab only.** A finding is reproduced on a local install with test
  accounts. Testing a third-party site without authorisation is not
  contribution, it is an incident.
- **Vendor first.** The vendor receives the full report — code location,
  impact, reproduction and remediation — before anything is published here.
- **Sanitised write-ups.** No weaponised payloads, no lab credentials, no
  live hostnames. The summary is what makes a finding readable; the exploit
  is not part of the write-up.
- **Dedupe first.** Check the vector against the CVE records, WPScan and the
  vendor's own changelog before treating it as new, and say in **Notes** what
  you checked against.
- **One finding per file.** Two products, two files.
- **No secrets.** Never commit API keys, tokens, passwords or personal data.
- **Match the existing style.** Follow the structure of the advisories already
  here; they are the template.

## Pull request rules

- **One change per PR.** Keep each pull request focused.
- **The validator must pass.** Run `python scripts/validate_advisories.py`
  before requesting review; CI must be green on the final commit.
- **Describe your change.** Say what changed, why, and how you tested it.

## Reporting bugs and requesting features

Use the GitHub issue templates (Bug report / Feature request) so reports
include the information needed to evaluate them.

## Reporting security vulnerabilities

Please do **not** open a public issue for a security vulnerability. Follow
the private reporting process in [SECURITY.md](SECURITY.md) instead.

## Code of conduct

Participation in this project is governed by the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Licence

By contributing, you agree that your contribution is provided under the
repository's existing licence.
