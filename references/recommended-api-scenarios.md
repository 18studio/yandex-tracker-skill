# Recommended Yandex Tracker API Scenarios

This document turns the local Tracker API notes into a practical set of recommended integration scenarios.
It is based on:

- `references/tracker-api.md`
- `references/documentation-pages.md`
- `README.md`
- the local helpers `scripts/tracker_api.py` and `scripts/tracker_scenario.py`

The recommendations below assume the common contract from the local docs:

- base URL: `https://api.tracker.yandex.net/v3`
- auth header: `Authorization: OAuth <token>` or `Authorization: Bearer <IAM token>`
- exactly one organization header:
  - `X-Org-ID: <org-id>`
  - `X-Cloud-Org-ID: <cloud-org-id>`

## How To Choose A Scenario

Start with the narrowest safe path:

1. Verify access and organization context.
2. Use read-only discovery before writes.
3. Use direct resource endpoints for single objects.
4. Use POST search endpoints for filtered selections and reports.
5. Use transitions for status changes.
6. Use scenario files for repeatable multi-step workflows.

## Recommended Scenario Set

### 1. Bootstrap And Access Check

Use this first for every new integration or environment.

Goal:

- confirm token validity
- confirm organization header type
- confirm the represented user
- confirm that the API surface is reachable

Recommended requests:

- `GET /myself`
- `GET /queues?perPage=100`

Why this is recommended:

- it validates the two most failure-prone integration dimensions first: auth and org scope
- it is fully read-only

Caveats:

- `401` usually means bad token format or expired token
- `403` usually means the user exists, but lacks Tracker permissions in the selected org

Best tool:

- `scripts/tracker_api.py` for one-off inspection
- `examples/bootstrap-discovery.json` for repeatable checks

### 2. Queue And Schema Discovery

Use this before issue creation or edits in a queue you do not control yet.

Goal:

- inspect queue metadata
- verify queue availability
- identify queue-local constraints before composing write payloads

Recommended requests:

- `GET /queues/<queue-key-or-id>`
- queue-local fields from the Queues API family in `references/documentation-pages.md`
- global fields and dictionaries from the Fields and Admin families when payload composition depends on them

Why this is recommended:

- Tracker payload failures often come from invalid field values, unknown local fields, or queue-specific workflow rules

Caveats:

- do not guess local-field names from another queue
- when exact field shape matters, inspect first and only then build the write payload

Best tool:

- `scripts/tracker_api.py`

### 3. Search Before Touching Issues

Use this as the default operating mode for bots, synchronizers, and reporting jobs.

Goal:

- locate the right issue set without hard-coding issue keys
- reduce accidental writes to the wrong objects
- drive follow-up reads or updates from a filtered selection

Recommended requests:

- `POST /issues/_search`
- `POST /issues/_count`
- `GET /issues/<issue-id>`

Why this is recommended:

- the local docs explicitly recommend POST-based search for non-trivial filtering
- it separates selection from mutation and makes automation safer

Caveats:

- design automations so empty search results are handled explicitly
- use direct `GET /issues/<id>` after search when you need the full issue payload

Best tool:

- `scripts/tracker_api.py` for ad hoc investigation
- `examples/issues-search-and-read.json` for repeatable selection flows

### 4. Issue Intake And Creation

Use this for service integrations, forms, mail-driven intake, and external event ingestion.

Goal:

- create issues from external systems in a controlled queue
- keep the payload minimal and deterministic

Recommended requests:

- `POST /issues`

Minimum safe body pattern:

```json
{
  "queue": "TEST",
  "summary": "Incoming request from external system",
  "type": {
    "key": "task"
  }
}
```

Why this is recommended:

- issue creation is the main integration entrypoint for operational automation
- a minimal body is easier to validate than a fully populated payload

Caveats:

- field availability is queue-dependent
- use YFM-compatible text where rich text is expected
- if creation depends on local fields, run queue/schema discovery first

Best tool:

- `scripts/tracker_api.py` for initial payload shaping
- `scripts/tracker_scenario.py` when creation is part of a longer workflow with assertions

### 5. Controlled Issue Updates

Use this after the issue already exists and you only need to edit fields, links, comments, or worklogs.

Goal:

- update issue content without replacing unrelated data
- use collection operators where the API expects them

Recommended requests:

- `PATCH /issues/<issue-id>`
- comments, links, checklist, attachment, and worklog endpoints from the Issues family

Why this is recommended:

- it keeps day-2 automation narrow and explicit
- it maps well to integration events such as sync, enrichment, or post-processing

Caveats:

- use collection operators such as `set`, `add`, `remove`, and `replace` where required by the field type
- attachments are not a single-step operation; plan for upload plus attach
- conflicts may appear as `409` or `412`

Best tool:

- `scripts/tracker_api.py`
- `scripts/tracker_scenario.py` when updates must be chained with validation

### 6. Status Changes Through Transitions

Use this whenever the target action is a workflow move, not a data edit.

Goal:

- move issues between statuses using the queue workflow rules

Recommended requests:

- `GET /issues/<issue-id>/transitions`
- `POST /issues/<issue-id>/transitions/<transition-id>/_execute`

Why this is recommended:

- the local docs explicitly say status must not be changed through a normal issue `PATCH`

Caveats:

- available transitions depend on current status and user permissions
- always read transitions first in automation that runs across multiple queues or workflows

Best tool:

- `scripts/tracker_api.py`
- `examples/issue-transition-check.json` for read-before-transition prechecks

### 7. Bulk Operations For High Volume Changes

Use this only when the same action must be applied to many issues.

Goal:

- avoid slow client-side loops for mass edits
- use Tracker-native async bulk processing

Recommended requests:

- bulk changes section from `references/documentation-pages.md`
- follow-up polling of bulk operation status/result endpoints

Why this is recommended:

- the local docs note that bulk operations are asynchronous and should be treated differently from ordinary issue updates

Caveats:

- do not assume immediate completion
- poll status or result endpoints explicitly
- apply the same read-first discipline as for single-issue edits

Best tool:

- `scripts/tracker_scenario.py`

### 8. Planning Entities: Projects, Portfolios, Goals

Use this for higher-level planning automation rather than task-by-task work.

Goal:

- read or create planning entities through the Entities API
- automate project creation inside a portfolio when the payload shape is known

Recommended requests:

- `GET /entities/portfolio/<portfolio-id>`
- `POST /entities/project`
- entity search endpoints from the Entities family when field expansion is required

Known-safe creation shape from local notes:

```json
{
  "fields": {
    "summary": "Infrastructure rollout",
    "parentEntity": "<portfolio-id>"
  }
}
```

Why this is recommended:

- the local repository already contains a validated scenario for project creation inside a portfolio

Caveats:

- keep business fields inside `fields`
- use `parentEntity` for linking a project to a portfolio
- do not infer create bodies for `portfolio` or `goal` from generic field docs when the local references do not confirm them
- direct reads such as `GET /entities/project/<id>` may not expose all business fields needed to reconstruct a create payload

Best tool:

- `examples/entities-project-in-portfolio.json`
- `scripts/tracker_scenario.py`

## Operational Recommendations

### Prefer `tracker_api.py` when

- you are exploring the API manually
- you need to inspect one resource quickly
- you are shaping a payload and want immediate feedback

### Prefer `tracker_scenario.py` when

- the workflow has multiple dependent steps
- you need assertions on response status or JSON fields
- you want reusable automation for CI, runbooks, or support operations
- you need conditional cleanup or saved variables between steps

## Scenario Design Rules

These rules are the most defensible defaults from the local docs:

- start every new integration with `GET /myself`
- prefer read-only discovery before mutation
- use POST search endpoints for filtered datasets
- use `PATCH` for field edits and transition endpoints for status changes
- treat attachments as a staged workflow, not a single request
- treat bulk updates as asynchronous
- for Entities API writes, only use field shapes confirmed by local references

## Suggested Adoption Order

Implement integrations in this order:

1. bootstrap and access check
2. queue and schema discovery
3. issue search and read
4. issue creation
5. issue update and comments
6. transitions
7. bulk operations
8. entities and higher-level planning automation

This order minimizes unknowns and matches the risk profile described in the local docs.
