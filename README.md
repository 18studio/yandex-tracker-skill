# Yandex Tracker

Skill and helper script for working with Yandex Tracker through the public REST API.

## Repository Contents

- `SKILL.md` defines the skill behavior, routing rules, and documentation workflow.
- `scripts/tracker_api.py` is a stdlib-only CLI for authenticated Tracker API requests.
- `scripts/tracker_scenario.py` runs reusable JSON-described API scenarios with variables, saved outputs, and assertions.
- `examples/` contains ready-to-run scenario files.
- `references/tracker-api.md` summarizes the core API contract and common pitfalls.
- `references/documentation-pages.md` maps API task areas to the local API reference index.
- `references/recommended-api-scenarios.md` contains the recommended operating scenarios for API integrations.
- `references/support-docs-index.md` maps product and UI questions to the current locally captured support-doc hierarchy.
- `references/tracker-docs-site-map.md` is the full Playwright-generated site map of the Tracker documentation menu.

## Requirements

- Python 3.11+
- A Yandex Tracker token:
  - `TRACKER_TOKEN` or `TRACKER_OAUTH_TOKEN`
  - `TRACKER_IAM_TOKEN`
- Exactly one organization header source:
  - `TRACKER_TRACKER_ORG_ID` or `TRACKER_ORG_ID`
  - `TRACKER_CLOUD_ORG_ID`

## Quick Start

Inspect the current user:

```bash
TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /myself
```

Fetch an issue:

```bash
TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/TEST-1
```

Search issues:

```bash
TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/_search \
  --method POST \
  --data '{"filter":{"queue":"TEST"}}'
```

Send query parameters and print headers:

```bash
TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /queues \
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

## `tracker_scenario.py`

Use the scenario runner when a task is better expressed as a repeatable workflow than as one-off `curl` commands.

What it supports:

- scenario file in JSON
- `{{var}}` substitution from environment, scenario vars, and `--var key=value`
- multiple sequential steps
- per-step request method, path, query, headers, body, or `body_file`
- status assertions and simple JSON-path-like assertions
- saving response values into variables for later steps
- conditional cleanup steps via `when`

Example:

```bash
TRACKER_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_scenario.py \
  examples/entities-project-in-portfolio.json \
  --var portfolio_id=123456 \
  --var project_summary="Infrastructure rollout" \
  --var delete_after_create=true
```

Minimal scenario shape:

```json
{
  "name": "Example scenario",
  "vars": {
    "issue_key": "TEST-1"
  },
  "steps": [
    {
      "name": "Read issue",
      "request": {
        "method": "GET",
        "path": "/issues/{{issue_key}}"
      },
      "expect": {
        "status": 200,
        "json": {
          "$.key": "TEST-1"
        }
      }
    }
  ]
}
```

Recommended starter scenarios:

- `examples/bootstrap-discovery.json` for auth, org, and queue reachability checks
- `examples/issues-search-and-read.json` for safe issue selection through POST search
- `examples/issue-transition-check.json` for read-before-transition workflow checks
- `examples/entities-project-in-portfolio.json` for the locally validated Entities API create flow

## Documentation Workflow

Use only the local markdown references:

1. Read `references/tracker-api.md` for API mechanics, headers, and update semantics.
2. Read `references/documentation-pages.md` to find the exact API family or method area.
3. Read `references/support-docs-index.md` for product behavior and UI workflows.
4. Use `references/tracker-docs-site-map.md` when you need the full documentation tree or need to verify exact menu placement.
5. If something seems missing, search the local `.md` files in `references/` instead of using the live Tracker site.

## Notes

- Status changes in Tracker are transitions, not ordinary issue field updates.
- Complex searches usually go through POST-based search endpoints.
- Attachments often require a temporary upload step before linking them to an issue or comment.
- API permissions match the rights of the represented user.
- Complex fields such as project, epic, and sprint often require nested object payloads rather than simple strings or numbers.
- For mass updates, validate one object first, then roll out in small batches with read-after-write verification.
- Links and dependencies are managed through dedicated `/links` endpoints and removed by link id, not by patching the issue body.
- Not every board supports sprint APIs; verify board capabilities before automating sprint assignment.
- Prefer stdlib-only tooling in this repository over external Python dependencies such as `requests`.

## License

MIT. See [LICENSE](./LICENSE).
