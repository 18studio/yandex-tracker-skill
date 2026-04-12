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

## Confirm Context

Collect these inputs when they are not already available:

- organization type: Yandex 360 or Yandex Cloud
- organization identifier: `X-Org-ID` or `X-Cloud-Org-ID`
- auth type: OAuth token or IAM bearer token
- target resource: issue, queue, board, dashboard, entity, user, field, or bulk operation

If the request is ambiguous, infer the smallest safe operation first, such as read-only inspection or search.

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
