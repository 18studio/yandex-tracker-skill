# Yandex Tracker

Skill and helper script for working with Yandex Tracker through the public REST API.

## Repository Contents

- `SKILL.md` defines the skill behavior, routing rules, and documentation workflow.
- `scripts/tracker_api.py` is a stdlib-only CLI for authenticated Tracker API requests.
- `references/tracker-api.md` summarizes the core API contract and common pitfalls.
- `references/documentation-pages.md` maps API task areas to official documentation pages.
- `references/support-docs-index.md` maps product and UI questions to the local support-site mirror.
- `references/support-site/en/` contains mirrored English support documentation pages.

## Requirements

- Python 3.11+
- A Yandex Tracker token:
  - `TRACKER_OAUTH_TOKEN` or `TRACKER_TOKEN`
  - `TRACKER_IAM_TOKEN`
- Exactly one organization header source:
  - `TRACKER_ORG_ID`
  - `TRACKER_CLOUD_ORG_ID`

## Quick Start

Inspect the current user:

```bash
TRACKER_OAUTH_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /myself
```

Fetch an issue:

```bash
TRACKER_OAUTH_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/TEST-1
```

Search issues:

```bash
TRACKER_OAUTH_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/_search \
  --method POST \
  --data '{"filter":{"queue":"TEST"}}'
```

Send query parameters and print headers:

```bash
TRACKER_OAUTH_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /queues \
  --query perPage=100 \
  --include-status
```

## `tracker_api.py`

The helper script:

- uses `https://api.tracker.yandex.net/v3` by default
- sends `Authorization` and exactly one organization header
- supports `--method`, `--query`, `--data`, `--data-file`, `--header`, `--raw`, and `--include-status`
- pretty-prints JSON responses by default
- exits non-zero on HTTP errors and still prints the error body

## Documentation Workflow

Use the local references before re-fetching external docs:

1. Read `references/tracker-api.md` for API mechanics, headers, and update semantics.
2. Read `references/documentation-pages.md` to find the exact API family or method page.
3. Read `references/support-docs-index.md` for product behavior and UI workflows.
4. Open the matching mirrored page in `references/support-site/en/` when the task depends on support documentation details.

## Notes

- Status changes in Tracker are transitions, not ordinary issue field updates.
- Complex searches usually go through POST-based search endpoints.
- Attachments often require a temporary upload step before linking them to an issue or comment.
- API permissions match the rights of the represented user.

## License

MIT. See [LICENSE](./LICENSE).
