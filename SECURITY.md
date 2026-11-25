# Security Policy

This repository holds sanitised security advisories. It contains no running
service, no exploitable code and no weaponised payloads, so what this policy
covers is the **accuracy of the write-ups** and the **privacy of the products
and people they describe** — not a live system.

## Reporting a vulnerability

Please **do not open a public issue** for a vulnerability. Report it
privately, either way:

- GitHub's private vulnerability reporting:
  <https://github.com/gravion-ux/security-research/security/advisories/new>
- Email: priyanshukumarthakur937@gmail.com

Please include:

- A one- or two-sentence description of the issue.
- The advisory file it affects, or the product and version if the advisory has
  not been written yet.
- The smallest reproduction you have — a sanitised description of the request
  or render path is ideal.
- The impact you believe it has.

You can expect an acknowledgement within a few days.

## Reporting a vulnerability in a product described here

If you find a vulnerability in **Kirki**, **Depicter**, or any other product
these advisories cover, do not report it in this repository. Report it to the
vendor, and you are welcome to open a discussion here afterwards.

## Disclosure timing

Please allow **90 days** for a fix to be released before any public
disclosure. If a fix ships earlier, coordinated disclosure can happen as soon
as the fixed version is available. Timing can be discussed — the goal is that
vendors are not left exposed.

## Scope

In scope — this repository, for example:

- An advisory that names a product, version or vendor incorrectly.
- A write-up that includes a weaponised payload, a live credential, or any
  other detail that should not be public.
- An advisory that describes testing that was not performed, or that implies a
  finding was confirmed against a production system.
- A link in an advisory that is broken or that points somewhere it should not.

Out of scope:

- The vulnerabilities described by the advisories themselves. Those belong to
  the affected vendors.
- Spelling and wording preferences that do not change what an advisory claims.
- Reports about other repositories in this account.

## Research standard

Every advisory here follows the same rules, and CI enforces the structural
part of them:

- Findings are reproduced on a **local lab** only. No third-party site is ever
  tested.
- The vendor is told **before** anything is published.
- Write-ups are **sanitised** — no payloads, no lab credentials.

If you believe an advisory in this repository breaks one of those rules,
please report it privately using the channel above.
