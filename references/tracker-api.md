# Yandex Tracker API Notes

## Base Contract

- Base URL: `https://api.tracker.yandex.net/v3`
- Main style: REST over JSON
- Auth header:
  - `Authorization: OAuth <token>`
  - `Authorization: Bearer <IAM token>`
- Organization header:
  - `X-Org-ID: <org-id>` for Yandex 360 organizations
  - `X-Cloud-Org-ID: <cloud-org-id>` for Yandex Cloud organizations

Send one auth header and one organization header on every request.

## Auth Model

- OAuth works for user-context access.
- IAM bearer tokens are used in Yandex Cloud setups.
- Service-account access in Cloud environments may require support-side enablement.
- API permissions match the represented user's Tracker permissions.

## Request Semantics

- Read operations usually use `GET`.
- Partial updates usually use `PATCH`.
- Creation usually uses `POST`.
- Complex searches often use POST endpoints such as `/_search` and `/_count`.
- Date-time values are expressed in UTC.
- Text fields use Yandex Flavored Markdown.

Tracker commonly uses collection operators in updates:

- `set`
- `add`
- `remove`
- `replace`

## Important Caveats

- Do not change issue status through a normal issue `PATCH`; use a transition endpoint.
- Attachments usually require an upload step that returns a temporary attachment identifier.
- Some objects use optimistic locking or version checks, so updates can fail with conflict-related responses.
- Bulk operations are asynchronous and usually require polling a status or result endpoint.

## Main Resource Families

### Issues

Use for day-to-day work on tasks:

- create issue
- get issue
- patch issue
- search issues
- count issues
- move issue
- transition issue
- get changelog
- manage comments
- manage checklist items
- manage links
- manage attachments
- manage worklog

### Queues

Use for queue-level configuration:

- get queue
- patch queue
- inspect local fields
- inspect components
- inspect versions
- inspect workflows and permissions

### Admin Dictionaries

Use for catalog and schema data:

- global fields
- field categories
- issue types
- statuses
- resolutions
- priorities
- users

### Boards and Dashboards

Use for work visualization:

- boards and columns
- dashboards and widgets

### Entities API

Use for newer planning entities:

- projects
- portfolios
- goals
- entity comments
- entity checklists
- entity events
- entity search with field expansion

## Common Request Templates

For live calls from this skill, use `scripts/tracker_api.py` with environment variables such as `TRACKER_TOKEN`, `TRACKER_OAUTH_TOKEN`, `TRACKER_IAM_TOKEN`, `TRACKER_TRACKER_ORG_ID`, `TRACKER_ORG_ID`, and `TRACKER_CLOUD_ORG_ID`.

### Search Issues

```http
POST /v3/issues/_search
Authorization: OAuth <token>
X-Org-ID: <org-id>
Content-Type: application/json
```

Use POST search for non-trivial filtering and pagination.

### Create Issue

```http
POST /v3/issues
Authorization: OAuth <token>
X-Org-ID: <org-id>
Content-Type: application/json
```

Minimum body usually includes queue, summary, and issue type.

### Edit Issue

```http
PATCH /v3/issues/<issue-id>
Authorization: OAuth <token>
X-Org-ID: <org-id>
Content-Type: application/json
```

Use update operators for collections when needed.

### Transition Issue

```http
POST /v3/issues/<issue-id>/transitions/<transition-id>/_execute
Authorization: OAuth <token>
X-Org-ID: <org-id>
Content-Type: application/json
```

Use this pattern when a task asks to change status.

## Error Patterns

Expect these categories:

- `400` for malformed payloads or incompatible field values
- `401` for invalid or missing auth
- `403` for missing permissions
- `404` for unknown resources
- `409` or `412` for conflicts or stale versions
- `423` when a resource is locked
- `429` for throttling

If a response shape matters, rely on this repository's local markdown references and report uncertainty explicitly when they are insufficient.
