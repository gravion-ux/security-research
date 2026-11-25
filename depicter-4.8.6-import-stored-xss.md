# Depicter ≤ 4.8.6 — Authenticated (Editor+) Stored XSS via Slider Import (Incomplete Fix of CVE-2026-113471)

| Field | Detail |
| --- | --- |
| Product | Depicter (WordPress slider / popup plugin) |
| Vendor | Averta |
| Affected versions | ≤ 4.8.6 (import code byte-identical in 4.8.5 and 4.8.6) |
| Vulnerability | Stored Cross-Site Scripting (CWE-79) via the slider import path |
| Required privilege | Editor (holds the plugin's `import_depicter` capability by default), without `unfiltered_html` |
| Severity | Medium — CVSS 3.1 5.4 (AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N), multisite framing |
| Disclosed | 23 Nov 2026, privately to the vendor (Averta) by email |
| Tested | Local lab only; no production site touched |

## Summary

The fix for CVE-2026-113471 (shipped in 4.8.5, extended in 4.8.6) sanitises
document content on the editor-save path and on the revision-revert path
whenever the saving user lacks the `unfiltered_html` capability. The
**slider import path was left out of that fix**: the import service takes
the content string from an uploaded package's data file and stores it
verbatim as a published document — no sanitisation pass, and no
`unfiltered_html` check of any kind. The only gate is the plugin's custom
import capability, which Depicter grants to the Editor role by default.

On WordPress multisite, Editors never hold `unfiltered_html`, so an Editor
who is correctly blocked from saving script content through the editor can
import the same content as a slider package and have it stored and
rendered — arbitrary JavaScript (element markup and scripted element
actions) executes for site visitors.

## Impact

An Editor-level account on a multisite network (or any install where
Editors are denied `unfiltered_html`) stores arbitrary JavaScript that
executes in the browsers of visitors and administrators viewing pages that
embed the slider — session/cookie theft, admin-action CSRF, defacement,
redirects. Sliders and popups are typically embedded site-wide, widening
exposure. On single-site installs with `DISALLOW_UNFILTERED_HTML` defined,
the render layer strips the script output, so impact there is limited to
verbatim storage.

## Reproduction (concept)

1. Sign in as an Editor (no `unfiltered_html`) and export any slider to
   learn the package format.
2. Build an import package whose document content carries a script payload
   in an element's content and/or in a scripted element action.
3. Import the package through the plugin's import endpoint. The import
   succeeds and creates a published document holding the content verbatim.
4. Embed the document in a page and visit it as an anonymous user: the
   payload renders and executes.

Negative control, verified in the lab: saving the identical content through
the editor-save path strips the script element and empties the scripted
action — the fixed path works; only import skips it. Verification used an
inert marker payload (JS comments only).

## Remediation

Apply the same treatment on import as on editor save: before storing, if
the importing user lacks `unfiltered_html`, run the decoded content through
the plugin's existing editor sanitiser and reject the import if it fails.
Alternatively, sanitise at render time based on the document author's
capabilities rather than only on a configuration constant.

## Notes

- This vector is an incomplete fix of CVE-2026-113471, shipped in 4.8.5 and
  extended in 4.8.6: the editor-save and revision-revert paths were
  sanitised, the slider import path was not. No public CVE or WPScan record
  covered the import path at disclosure time.
- The vendor was contacted by email on 23 Nov 2026; a lab re-test of any fix
  was offered.
