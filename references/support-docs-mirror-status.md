# Tracker Support Docs Status

This repository no longer stores local HTML copies of the Yandex Tracker support site.

## Current State

- local HTML pages in repo: 0
- support reference source: `https://yandex.ru/support/tracker/en/`
- local support reference file: `references/support-docs-index.md`
- migration date: 2026-04-12

## Historical Aliases

Two legacy English routes have been seen in older references. Prefer the canonical pages:

- `manager/create-project.html` -> `manager/project-new.html`
- `manager/access.html` -> `access.html`

## How To Handle A Suspicious Page

If a support page looks wrong or stale:

1. Start with [support-docs-index.md](support-docs-index.md).
2. Prefer the canonical route when an alias is listed above.
3. Search the local markdown references with `rg -n "keyword" references/*.md SKILL.md README.md`.
4. Fall back to the live support site only when the markdown references are insufficient.
