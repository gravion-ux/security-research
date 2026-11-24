# Kirki ≤ 6.4.3 — Authenticated (Editor+) Stored XSS in Select / Radio-Group Rendering

| Field | Detail |
| --- | --- |
| Product | Kirki — Freeform Page Builder, Website Builder & Customizer (WordPress plugin, slug `kirki`) |
| Vendor | Themeum |
| Affected versions | ≤ 6.4.3 (latest at time of testing; 400,000+ active installs) |
| Vulnerability | Stored Cross-Site Scripting (CWE-79) |
| Required privilege | Editor (Kirki editor access), without `unfiltered_html` |
| Severity | Medium — CVSS 3.1 ≈ 6.4 (estimated) |
| Disclosed | 23 Nov 2026, privately to the vendor by email |
| Tested | Local lab only (WordPress 7.1.5 + Kirki 6.4.3); no production site touched |

## Summary

Kirki's front-end page renderer outputs Select-element option values and
labels, and Radio-Group option values and labels, without escaping. An
Editor who has Kirki editor access — but who, on a multisite install or a
site defining `DISALLOW_UNFILTERED_HTML`, does **not** hold the
`unfiltered_html` capability — can store a malicious option value or label
through the normal page editor. The stored content is then rendered
unescaped on the published page, executing in the browser of every visitor,
including administrators.

Neighbouring renderers in the same codebase escape their output correctly
(attribute output elsewhere uses `esc_attr()`, and the checkbox renderer
only interpolates integer IDs), which makes the Select and Radio-Group
renderers in `includes/Frontend/Preview/ExceptionalElements.php` look like
missed spots rather than a design choice. Option values and labels are saved
through the plugin's page-save path into post meta with no sanitisation of
block properties, and Kirki's own role map grants Editors editor access.

## Impact

Stored XSS executed for every visitor viewing a published Kirki page that
contains a malicious Select or Radio-Group option: session hijacking,
actions performed as a viewing administrator, defacement, phishing. On
single-site installs Editors normally hold `unfiltered_html` and the impact
is lower; the multisite / `DISALLOW_UNFILTERED_HTML` case is the genuine
privilege-boundary violation, because the affected user class is explicitly
denied raw-HTML capability by WordPress core.

## Reproduction (concept)

1. Sign in as an Editor on a site where Editors lack `unfiltered_html`.
2. Create or edit a Kirki page and add a Select element (or a Radio Group),
   setting an option value or label that breaks out of the rendered
   attribute / element context with an HTML event-handler construct.
3. Publish the page and view it as an unauthenticated visitor.
4. The option markup is emitted unescaped and the injected construct
   executes on page view.

Verified in the lab with all four sinks (Select value, Select label,
Radio-Group value, Radio-Group label) rendering unescaped.

## Remediation

Escape on output in both renderers — `esc_attr()` for option values and
element names, `esc_html()` for option labels and content — and ideally
sanitise option values and labels on save as defence in depth.

## Notes

- This vector is distinct from CVE-2026-115814 (≤ 6.4.1) and WPSEC-2026-3702
  (≤ 6.4.2, fixed in 6.4.3); no public CVE/WPScan record covered this vector
  at disclosure time.
- The vendor was contacted by email on 23 Nov 2026 after their web contact
  form rejected the submission twice; a lab re-test of any fix was offered.
