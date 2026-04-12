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

### Entities API Quick Notes

These shapes are worth treating as the local default until the docs provide a more explicit per-entity schema reference:

- Read a portfolio by id with `GET /v3/entities/portfolio/<id>`.
- Create a project with `POST /v3/entities/project`.
- For project creation, put business fields inside `{"fields": {...}}`.
- To attach a project to a portfolio, set `fields.parentEntity` to the portfolio entity id.
- Do not assume `GET /v3/entities/project/<id>` returns enough business fields to reconstruct a valid create payload.
- If `GET /entities/project/<id>` only returns wrapper metadata, use entity search or another expanded entity endpoint from the local docs before guessing field names.

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

### Read Portfolio Entity

```http
GET /v3/entities/portfolio/<portfolio-id>
Authorization: OAuth <token>
X-Org-ID: <org-id>
```

This is the singular entity route. Do not switch it to `/portfolios/`.

CLI example:

```bash
TRACKER_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /entities/portfolio/<portfolio-id>
```

cURL example:

```bash
curl -sS \
  -H "Authorization: OAuth $TRACKER_TOKEN" \
  -H "X-Org-ID: $TRACKER_ORG_ID" \
  "https://api.tracker.yandex.net/v3/entities/portfolio/<portfolio-id>"
```

### Create Project In Portfolio

```http
POST /v3/entities/project
Authorization: OAuth <token>
X-Org-ID: <org-id>
Content-Type: application/json

{
  "fields": {
    "summary": "Infrastructure rollout",
    "parentEntity": "<portfolio-id>"
  }
}
```

Known-safe rules from live usage:

- `summary` belongs inside `fields`.
- portfolio linkage is `parentEntity`, not `portfolio`, `portfolioId`, or `parent`.
- top-level payloads without `fields` can produce misleading validation errors.

CLI example:

```bash
TRACKER_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /entities/project \
  --method POST \
  --data '{"fields":{"summary":"Infrastructure rollout","parentEntity":"<portfolio-id>"}}'
```

cURL example:

```bash
curl -sS \
  -X POST \
  -H "Authorization: OAuth $TRACKER_TOKEN" \
  -H "X-Org-ID: $TRACKER_ORG_ID" \
  -H "Content-Type: application/json" \
  --data '{"fields":{"summary":"Infrastructure rollout","parentEntity":"<portfolio-id>"}}' \
  "https://api.tracker.yandex.net/v3/entities/project"
```

### Delete Mistakenly Created Project

```http
DELETE /v3/entities/project/<project-id>
Authorization: OAuth <token>
X-Org-ID: <org-id>
```

CLI example:

```bash
TRACKER_TOKEN=... TRACKER_ORG_ID=... ./scripts/tracker_api.py /entities/project/<project-id> \
  --method DELETE
```

cURL example:

```bash
curl -sS \
  -X DELETE \
  -H "Authorization: OAuth $TRACKER_TOKEN" \
  -H "X-Org-ID: $TRACKER_ORG_ID" \
  "https://api.tracker.yandex.net/v3/entities/project/<project-id>"
```

## Entity-Field Caveats

The local reference set currently explains the Entities API family, but does not provide a reliable field matrix with concrete create bodies for every entity type.

Treat these points as operational guidance:

- `project`: locally confirmed working fields include `summary` and `parentEntity` inside `fields`.
- `portfolio`: local docs confirm the entity family, but this repository does not currently contain a verified minimal create/update body example.
- `goal`: local docs confirm the entity family, but this repository does not currently contain a verified minimal create/update body example.

When exact field availability matters for `portfolio` or `goal`, do not invent a body from the generic `/fields` family. Use the local entity docs plus a safe read/search flow to confirm the shape first.

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

Entities API errors can be especially misleading. Invalid nesting may be reported as a problem with `fields` or `summary` even when the real issue is a wrong parent-link field or an incorrect top-level payload shape.
