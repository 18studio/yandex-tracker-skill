# Tracker Support Docs Status

This repository does not store local HTML copies of the Yandex Tracker support site.
The local source of truth is the markdown generated from the captured navigation tree.

## Current State

- local HTML pages in repo: `0`
- support reference source used for the last capture: `https://yandex.ru/support/tracker/en/about-tracker`
- generated tree file: [tracker-docs-site-map.md](tracker-docs-site-map.md)
- working support index: [support-docs-index.md](support-docs-index.md)
- last menu capture: `2026-04-12T13:57:38.742Z`

## Notes

- The live root page `https://yandex.ru/support/tracker/en/` was not a reliable crawl seed in this environment.
- The stable capture source was the fully rendered left navigation menu on `about-tracker`.
- Route assumptions from older hand-written references should not be treated as canonical unless they also appear in [tracker-docs-site-map.md](tracker-docs-site-map.md).

## How To Handle Gaps

1. Start with [support-docs-index.md](support-docs-index.md).
2. If you need the full hierarchy, inspect [tracker-docs-site-map.md](tracker-docs-site-map.md).
3. Search the local markdown references with `rg -n "keyword" references/*.md SKILL.md README.md`.
4. If local markdown is still insufficient, state that limitation explicitly instead of browsing the live site.
