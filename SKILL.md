---
name: Yandex Tracker
description: "Manage Yandex Tracker spaces through the REST API. Use when Codex needs to work with any documented Tracker API function: issues, issue filters, checklists, comments, attachments, bulk operations, fields, projects, portfolios, goals, queues, automation, boards, dashboards, components, issue types, statuses, resolutions, priorities, worklogs, imports, links to external applications, or users in a Yandex Tracker organization."
---

# Yandex Tracker

Use this skill to work with a Yandex Tracker space through the public API and the local markdown references in this repository.

## Read Order

Choose the documentation source by task type:

1. For Tracker product behavior and UI workflows, start with [references/support-docs-index.md](references/support-docs-index.md).
2. For REST API work, start with [references/tracker-api.md](references/tracker-api.md), then use [references/documentation-pages.md](references/documentation-pages.md) to jump to the exact API family or method page.
3. Do not browse the live Tracker site. Use only the local markdown files under `references/` and this `SKILL.md`.
4. If the local markdown looks incomplete, search the local repository references instead of falling back to external docs.

## Which File To Read First

Use this routing table before answering a user task:

- queue setup, permissions, local fields, components, versions, mail integration, workflow editing:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Configuring queues" section
- issue creation and daily work such as editing, moving, comments, attachments, links, checklists, reminders, votes, history, and time spent:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Working with issues" section
- issue search, filters, favorites, summaries, and list views:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Finding issues" section
- dashboards, widgets, reports, and monitoring:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Dashboards and widgets" section and "Reports" when needed
- automation, triggers, auto actions, macros, notifications, and mail notifications:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Automations" section and "Notifications and subscriptions" when needed
- agile boards, sprints, burndown, planning poker, and board permissions:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Managing issues using an Agile board" section
- projects, portfolios, goals, epics, milestones, and gantt:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Projects, portfolios, and goals" section and "Gantt chart" when needed
- templates, forms, mail intake, and form integrations:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Issue and comment templates" section and "Integration with other services" when needed
- markdown, YFM, tables, diagrams, images, embedded content, and rich formatting:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Working with issues" section under "Editing text"
- mobile app or Messenger behavior:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Yandex Tracker mobile app" section
- imports, developer tools, troubleshooting, browser console, HAR, and support diagnostics:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Developer tools" section, "Integration with other services" section, and "Enabling and managing access" for import-related setup
- API endpoints, headers, payloads, permissions, pagination, transitions, or field schemas:
  read [references/tracker-api.md](references/tracker-api.md) first, then [references/documentation-pages.md](references/documentation-pages.md)

Use [references/tracker-docs-site-map.md](references/tracker-docs-site-map.md) when you need the full product-doc hierarchy or need to verify where a page sits in the menu.
Use [references/support-docs-mirror-status.md](references/support-docs-mirror-status.md) only for notes about the local capture process. It is not a permission to browse the live support site.

## Workflow

1. Identify the organization context before proposing requests.
2. Confirm the auth mode and required headers.
3. Choose the narrowest API resource that matches the task.
4. Use only local markdown references from this repository.
5. When making changes, explain the exact request shape, required permissions, and likely failure modes.

## Operating Principles

Use these working rules whenever the task involves live Tracker changes:

- Prefer stdlib-only tooling from this repository. Use [scripts/tracker_api.py](scripts/tracker_api.py) and [scripts/tracker_scenario.py](scripts/tracker_scenario.py) before suggesting ad hoc scripts with external dependencies.
- Do not assume Tracker field shapes from UI labels or common REST conventions. Verify the exact payload shape for each non-trivial field before scaling to bulk updates.
- Separate discovery, mutation, and verification. Read first, change second, verify third.
- Prefer small, reversible batches over one long bulk run.
- If a multi-step update partially succeeds, inspect actual Tracker state before retrying anything.
- When a user asks for large structural changes, preserve existing issue keys and entity ids when possible; prefer reclassification over delete-and-recreate.

## Confirm Context

Collect these inputs when they are not already available:

- organization type: Yandex 360 or Yandex Cloud
- organization identifier: `X-Org-ID` or `X-Cloud-Org-ID`
- auth type: OAuth token or IAM bearer token
- target resource: issue, queue, board, dashboard, entity, user, field, or bulk operation

If the request is ambiguous, infer the smallest safe operation first, such as read-only inspection or search.

## Practical Playbook

Follow this sequence for work that changes issues, links, projects, portfolios, or boards:

1. Discover the current state with read-only calls.
2. Validate one field or one relationship on a single object.
3. Promote the confirmed payload shape into a small batch.
4. Verify the batch by reading objects back by key or id.
5. Only then continue with the next batch.

For risky changes, prefer this split:

- create with the smallest valid payload
- patch additional fields afterward
- verify the final shape with a read call

For search-dependent workflows:

- treat search as a convenience, not as the only source of truth
- if `_search` is unstable for the task, fall back to known issue keys or known entity ids
- prefer deterministic key-by-key verification after bulk updates

## Coverage

This skill is intended to cover the full public Tracker API documentation surface, not only the common issue endpoints.

Treat these documentation families as in scope:

- issues
- issue filters
- issue checklists
- issue comments
- issue attachments
- bulk issue operations
- issue fields and field categories
- projects, portfolios, and goals
- legacy projects endpoints when a task explicitly needs them
- queues and queue-local fields
- automation objects such as triggers, macros, and actions
- boards and columns
- dashboards and widgets
- components
- issue types, statuses, resolutions, and priorities
- time tracking and worklogs
- import endpoints
- links with external applications
- users and current-user identity

## Use Local References

Read [references/tracker-api.md](references/tracker-api.md) for the core API contract:

- base URL and headers
- auth rules
- update semantics
- resource families
- common flows and pitfalls

Read [references/documentation-pages.md](references/documentation-pages.md) when you need the relevant API family quickly. It groups the documented API surface by task area and preserves the route names for orientation.

Read [references/support-docs-index.md](references/support-docs-index.md) when the task is about using Tracker itself rather than just calling the API. It mirrors the current left-menu hierarchy from the captured product docs.

Read [references/tracker-docs-site-map.md](references/tracker-docs-site-map.md) when you need the complete expanded tree or want to verify whether a page exists in the captured docs.

Use [scripts/tracker_api.py](scripts/tracker_api.py) for real API calls. It is a stdlib-only CLI helper that:

- sends the required `Authorization` header
- sends either `X-Org-ID` or `X-Cloud-Org-ID`
- accepts a path like `/myself` or `/issues/TEST-1`
- supports `--method`, `--query`, `--data`, `--data-file`, `--header`, and `--raw`
- reads credentials from environment variables when present

Use [scripts/tracker_scenario.py](scripts/tracker_scenario.py) when the task is a repeatable multi-step API workflow rather than a single request. It supports:

- JSON-described scenarios under `examples/` or user-created files
- `{{var}}` substitution from env, scenario vars, and CLI `--var key=value`
- sequential steps with assertions and saved response values
- conditional cleanup steps through `when`

## Request Rules

Apply these rules consistently:

- Use `https://api.tracker.yandex.net/v3` unless a task explicitly requires a legacy version.
- Send `Authorization` plus exactly one organization header: `X-Org-ID` or `X-Cloud-Org-ID`.
- Treat issue status changes as transitions, not ordinary `PATCH` updates.
- Use POST-based search endpoints for complex issue and entity searches.
- For attachments, account for the temporary upload step before attaching to an issue or comment.
- Respect Tracker permissions. API tokens act with the same rights as the represented user.
- For `POST /entities/project`, send business data under `{"fields": {...}}`, not at the top level.
- For linking a project to a portfolio, use `fields.parentEntity` with the portfolio entity id.
- For direct entity reads, prefer singular routes such as `/entities/project/<id>` and `/entities/portfolio/<id>`.
- Do not assume `GET /entities/project/<id>` returns the full business payload. When field shape matters, use entity search or another expanded read path from the local docs.

## Field Shape Rules

Tracker often rejects "obvious" payloads for complex fields. Treat field encoding as a first-class concern.

- For object-backed fields, expect nested objects such as `{"id":"..."}` or `{"key":"..."}`, not bare strings.
- For multi-value relations, expect arrays of objects, not a single scalar.
- Validate each field independently before combining several complex fields in one create or patch request.
- When a field fails with `400` or `422`, remove all optional fields, re-add them one by one, and keep the first confirmed working shape.

Examples that were validated in practice:

- `project`: `{"id":"28"}`
- `epic`: `{"key":"DEV-2"}`
- `sprint`: `[{"id":"4"}]`

Do not generalize one field's shape to another field family without checking the docs or a live test.

## Search Rules

Issue and entity search endpoints can be sensitive to body shape.

- Prefer documented structured JSON bodies over free-form query strings.
- When debugging a failing search, first reduce the request to the smallest filter that should match.
- If a bulk workflow depends on `_search` and the endpoint starts returning `400`, do not keep retrying the same shape blindly.
- Fall back to stable identifiers such as known issue keys, project ids, portfolio ids, or entity ids.
- For high-confidence verification, read objects directly by key or id after mutation.

## Create And Patch Strategy

Use a conservative write strategy for create-heavy workflows:

- create issues and entities with the smallest payload that is known to pass validation
- add secondary fields in follow-up `PATCH` requests
- keep links, sprint assignment, epic assignment, and other relationship-like updates separate when possible
- avoid "all fields at once" payloads unless the exact shape was already confirmed in this Tracker space

This is the default response to `422 Unprocessable Entity`: simplify the payload, confirm the base create works, then layer fields back in.

## Bulk Safety Rules

For mass renames, rescheduling, migration, or portfolio reshaping:

- never rely on a single long-running script as the only control mechanism
- break work into small batches
- verify each batch before proceeding
- if a script stops mid-run, inspect actual state before rerunning anything
- avoid blind retries that can duplicate issues, duplicate links, or overwrite correct fields
- prefer short verification passes keyed by known issue keys or entity ids

If a process appears to hang:

- assume partial success is possible
- verify a sample of target objects immediately
- continue with targeted follow-up scripts rather than rerunning the full batch

## Links And Dependencies

Treat issue links as a separate API surface, not as a normal issue field.

- Create links through `/issues/<key>/links`.
- Use the documented `relationship` value, for example `dependsOn`.
- Test one link first before creating many links.
- Read links back after creation to confirm both direction and link id.
- Delete incorrect links only through their concrete link id, not by patching the issue body.

Example create shape:

```json
{"relationship":"dependsOn","issue":"DEV-16"}
```

Example delete path shape:

```text
DELETE /issues/DEV-15/links/49
```

## Boards And Sprints

Do not assume every board that looks agile in the UI supports sprint API methods.

- Verify the target board type before planning sprint operations.
- If the API reports that the board type cannot have sprints, stop using that board for sprint automation.
- Keep project boards for reporting or visualization if needed, but use a sprint-capable board for delivery planning.

## Projects, Portfolios, And Entities

Entity APIs are less predictable than issue APIs. Use stable identifiers and verify business fields explicitly.

- Prefer known project ids, portfolio ids, and entity ids over repeated lookup by title.
- After updates, verify fields such as dates, parent linkage, and ids instead of relying only on `summary`.
- When creating projects in a portfolio, start from the safe payload shape documented in local references and extend cautiously.

## Error Handling

Use HTTP status codes as debugging signals, not just failures:

- `400 Bad Request`: likely wrong endpoint shape, malformed search body, unsupported board operation, or invalid field encoding.
- `422 Unprocessable Entity`: endpoint accepted the request form, but one or more field values or combinations are invalid for this queue or entity type.

Recommended response:

1. Reduce the request to the smallest possible body.
2. Reintroduce complex fields one at a time.
3. Read back the resulting object after each successful mutation.
4. Preserve the working payload shape for reuse in the next batch.

## Environment Constraints

Assume the runtime may be minimal.

- Do not depend on `requests` being installed.
- Prefer `scripts/tracker_api.py`, `scripts/tracker_scenario.py`, or stdlib-based `urllib.request` for diagnostics and automation.
- If the environment lacks a convenience library, adapt the script instead of blocking on package installation.

## Common Tasks

### Issues

- search issues
- create or edit issues
- move issues between queues
- transition issue status
- manage comments, links, checklists, attachments, and worklogs

### Space Configuration

- inspect queues and queue-local fields
- inspect or create global fields
- inspect issue types, statuses, resolutions, and priorities
- inspect boards, columns, dashboards, and widgets
- inspect automation resources, components, and imports

### Higher-Level Planning Objects

- work with projects, portfolios, and goals through the Entities API
- search entities and fetch expanded field payloads
- for project creation inside a portfolio, start from the known-safe shape in [references/tracker-api.md](references/tracker-api.md) instead of inferring field names ad hoc

### Full-API Requests

When a task references a less common API area, do not fall back to generic guidance. Open the matching section from [references/documentation-pages.md](references/documentation-pages.md), identify the exact method area, and answer from the local references.

## Output Style

When answering a Tracker task:

- name the exact endpoint and method
- list the required headers
- show the minimal request body
- mention any Tracker-specific caveat such as transitions, pagination, optimistic locking, or permissions
- explain whether the operation should be tested first on one issue, one entity, or one board before bulk rollout
- if field shape is non-obvious, call it out explicitly instead of implying a generic JSON patch will work
- if the request is bulk or high-risk, include a verification step and fallback plan
- cite the local markdown file that the answer relies on

## Script Examples

Use the helper script for repeatable live calls:

```bash
TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /myself
```

```bash
TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/TEST-1
```

```bash
TRACKER_TOKEN=... TRACKER_TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/_search \
  --method POST \
  --data '{"filter":{"queue":"TEST"}}'
```
