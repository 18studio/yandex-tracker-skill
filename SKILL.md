---
name: Yandex Tracker
description: "Manage Yandex Tracker spaces through the REST API. Use when Codex needs to work with any documented Tracker API function: issues, issue filters, checklists, comments, attachments, bulk operations, fields, projects, portfolios, goals, queues, automation, boards, dashboards, components, issue types, statuses, resolutions, priorities, worklogs, imports, links to external applications, or users in a Yandex Tracker organization."
---

# Yandex Tracker

Use this skill to work with a Yandex Tracker space through the public API and its documentation.

## Read Order

Choose the documentation source by task type:

1. For Tracker product behavior and UI workflows, start with [references/support-docs-index.md](references/support-docs-index.md).
2. For REST API work, start with [references/tracker-api.md](references/tracker-api.md), then use [references/documentation-pages.md](references/documentation-pages.md) to jump to the exact API family or method page.
3. For the actual article text, follow the official support page link from [references/support-docs-index.md](references/support-docs-index.md).
4. If a support page looks wrong, stale, too short, or suspicious, check [references/support-docs-mirror-status.md](references/support-docs-mirror-status.md) for canonical route guidance before trusting it.

## Which File To Read First

Use this routing table before answering a user task:

- queue setup, permissions, local fields, components, versions, mail integration, workflow editing:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Queues and Queue Administration" section, then the exact official support page link
- issue creation and daily work such as editing, moving, comments, attachments, links, checklists, reminders, votes, history, and time spent:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Everyday Work With Issues" section, then the exact official support page link
- issue search, filters, favorites, summaries, and list views:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Search, Filters, Lists, and Views" section
- dashboards, widgets, reports, and monitoring:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Dashboards, Widgets, and Reports" section
- automation, triggers, auto actions, macros, notifications, and mail notifications:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Automation, Triggers, Macros, and Notifications" section
- agile boards, sprints, burndown, planning poker, and board permissions:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Agile Boards, Sprints, Planning, and Estimation" section
- projects, portfolios, goals, epics, milestones, and gantt:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Projects, Portfolios, Goals, Milestones, and Gantt" section
- templates, forms, mail intake, and form integrations:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Templates, Forms, and Intake" section
- markdown, YFM, tables, diagrams, images, embedded content, and rich formatting:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Markdown and Rich Content" section
- mobile app or Messenger behavior:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Mobile and Messenger" section
- imports, developer tools, troubleshooting, browser console, HAR, and support diagnostics:
  read [references/support-docs-index.md](references/support-docs-index.md), then the "Import, External Links, API, and Troubleshooting" section
- API endpoints, headers, payloads, permissions, pagination, transitions, or field schemas:
  read [references/tracker-api.md](references/tracker-api.md) first, then [references/documentation-pages.md](references/documentation-pages.md), then the exact official API page

Use [references/support-docs-mirror-status.md](references/support-docs-mirror-status.md) whenever a support page route might be stale. Note that `manager/create-project.html` and `manager/access.html` are historical aliases; prefer their canonical pages noted in that file.

## Workflow

1. Identify the organization context before proposing requests.
2. Confirm the auth mode and required headers.
3. Choose the narrowest API resource that matches the task.
4. Prefer reading local references before browsing docs again.
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

Read [references/documentation-pages.md](references/documentation-pages.md) when you need the relevant documentation page quickly. It groups the official docs by task area and links to the section roots and representative method pages.

Read [references/support-docs-index.md](references/support-docs-index.md) when the task is about using Tracker itself rather than just calling the API. It maps user tasks to the official English support pages.

Use [scripts/tracker_api.py](scripts/tracker_api.py) for real API calls. It is a stdlib-only CLI helper that:

- sends the required `Authorization` header
- sends either `X-Org-ID` or `X-Cloud-Org-ID`
- accepts a path like `/myself` or `/issues/TEST-1`
- supports `--method`, `--query`, `--data`, `--data-file`, `--header`, and `--raw`
- reads credentials from environment variables when present

## Request Rules

Apply these rules consistently:

- Use `https://api.tracker.yandex.net/v3` unless a task explicitly requires a legacy version.
- Send `Authorization` plus exactly one organization header: `X-Org-ID` or `X-Cloud-Org-ID`.
- Treat issue status changes as transitions, not ordinary `PATCH` updates.
- Use POST-based search endpoints for complex issue and entity searches.
- For attachments, account for the temporary upload step before attaching to an issue or comment.
- Respect Tracker permissions. API tokens act with the same rights as the represented user.

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

### Full-API Requests

When a task references a less common API area, do not fall back to generic guidance. Open the matching section from [references/documentation-pages.md](references/documentation-pages.md), identify the exact method page, and answer against that page.

## Output Style

When answering a Tracker task:

- name the exact endpoint and method
- list the required headers
- show the minimal request body
- mention any Tracker-specific caveat such as transitions, pagination, optimistic locking, or permissions
- link the official documentation page when the request depends on details that may change

## Script Examples

Use the helper script for repeatable live calls:

```bash
TRACKER_OAUTH_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /myself
```

```bash
TRACKER_OAUTH_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/TEST-1
```

```bash
TRACKER_OAUTH_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /issues/_search \
  --method POST \
  --data '{"filter":{"queue":"TEST"}}'
```
