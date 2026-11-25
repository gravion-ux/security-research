## What changed

<!-- One or two sentences. What is different after this pull request? -->

## Why

<!-- The problem this solves. For a new advisory: the finding, the product and
     the version. For a correction: the claim that was wrong. -->

## How it was tested

<!-- The exact command you ran and what it printed, e.g.
     `python scripts/validate_advisories.py` followed by the validator's
     summary line. -->

## Disclosure status

<!-- For a new advisory: when the vendor was told and how. If the vendor has
     not been contacted yet, say so -- a public write-up before disclosure is
     not acceptable, and the pull request should stay a draft. -->

## Sanitisation

<!-- Confirm the diff carries no weaponised payload, no credential, no live
     hostname, and no lab detail that identifies a test target. -->

## Checklist

- [ ] `python scripts/validate_advisories.py` passes locally and CI is green
- [ ] The advisory has a Summary table with Product, Affected versions, Vulnerability, Severity and Disclosed
- [ ] The advisory has the Summary, Impact, Reproduction, Remediation and Notes sections
- [ ] The vendor was told before publication
- [ ] The finding was reproduced on a local lab; no third-party site was tested
- [ ] No weaponised payload, credential, or live target anywhere in the diff
- [ ] The README advisory table lists the new advisory, with a working link
- [ ] One logical change in this PR
