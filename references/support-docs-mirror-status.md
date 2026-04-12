# Tracker Support Mirror Status

The local support mirror is stored under `references/support-site/en/`.

## Current Snapshot

- language: English
- source root: `https://yandex.ru/support/tracker/en/`
- mirrored HTML pages: 191
- refresh method for anti-bot pages: `playwright-skill` via live browser fetch on 2026-04-12
- known captcha markers remaining in mirror: 0
- known 404 pages remaining in mirror: 0

## Mirror Health

Most pages now contain the real article body. A Playwright refresh replaced the previously captured captcha pages for the main problematic URLs.

## Alias Backfills

Two saved paths do not currently have stable live English routes, so the local mirror stores canonical English article content under these legacy paths:

- `references/support-site/en/manager/create-project.html`
- `references/support-site/en/manager/access.html`

Backfill sources:

- `references/support-site/en/manager/create-project.html` was backfilled from `references/support-site/en/manager/project-new.html`
- `references/support-site/en/manager/access.html` was backfilled from `references/support-site/en/access.html`

Each of these files starts with an HTML comment documenting the canonical source page and save timestamp.

## How To Handle A Suspicious Page

If a mirrored page looks wrong:

1. Read the nearest overview page from [support-docs-index.md](support-docs-index.md).
2. Prefer the canonical neighboring page for the same feature area.
3. Search the mirror with `rg -n "keyword" references/support-site/en`.
4. Fall back to the live documentation page only when the local mirror remains incomplete.

## Notes

The mirror is intended to be the default source for Tracker product documentation. At the moment, the local English mirror has no known captcha or 404 pages, and the two previously broken paths have been backfilled with canonical content.
