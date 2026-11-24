# Security Research — Priyanshu Kumar Thakur (GRAVION)

Write-ups of vulnerabilities I found, verified in a local lab, and disclosed
responsibly to the affected vendor. Nothing here was tested against a
production site: every finding was reproduced against a local WordPress
install, reported to the vendor first, and published here only in sanitised
advisory form.

**Researcher:** Priyanshu Kumar Thakur · [github.com/gravion-ux](https://github.com/gravion-ux) · [Portfolio](https://gravion-ux.github.io/portfolio/)

## Advisories

| # | Product | Vulnerability | Affected | Severity | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | [Kirki (WordPress plugin)](kirki-6.4.3-editor-stored-xss.md) | Authenticated (Editor+) Stored XSS in Select / Radio-Group rendering (CWE-79) | ≤ 6.4.3 | Medium (CVSS ~6.4) | Disclosed to Themeum, 23 Nov 2026 |
| 2 | [Depicter (WordPress plugin)](depicter-4.8.6-import-stored-xss.md) | Authenticated (Editor+) Stored XSS via slider import — incomplete fix of CVE-2026-113471 | ≤ 4.8.6 | Medium (CVSS 5.4) | Disclosed to Averta, 23 Nov 2026 |

## Method

1. **Local lab only.** Findings are reproduced on a local WordPress install
   with test accounts. No third-party site is ever tested.
2. **Dedupe first.** Each vector is checked against CVE records, WPScan and
   the vendor's own changelog before it is treated as new.
3. **Vendor first.** The vendor receives the full report — code location,
   impact, reproduction and remediation — before anything is published.
4. **Sanitised write-ups.** These summaries carry the summary, affected
   versions, impact, reproduction concept and remediation a standard
   advisory carries — no weaponised payloads, no lab credentials.

## Scope note

Both findings require an authenticated Editor-level account and matter most
where Editors are denied the `unfiltered_html` capability — WordPress
multisite, or installs with `DISALLOW_UNFILTERED_HTML` defined. That is the
privilege boundary each one crosses: a user the platform deliberately keeps
away from raw HTML gets script execution anyway.
