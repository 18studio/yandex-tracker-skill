# Tracker API Documentation Pages

This page indexes the official Yandex Tracker API documentation so the skill can jump to the right section quickly.
It is organized to match the documentation navigation and to cover the whole public API surface.

## Core Pages

- API overview: `https://yandex.ru/support/tracker/ru/api-ref/about-api`
- API access: `https://yandex.ru/support/tracker/ru/api-ref/access`
- Common request format: `https://yandex.ru/support/tracker/ru/api-ref/common-format`
- Error codes: `https://yandex.ru/support/tracker/ru/api-ref/error-codes`

## Issues

Use this area for issue lifecycle operations.

- create issue: `https://yandex.ru/support/tracker/ru/api-ref/issues/create-issue`
- get issue: `https://yandex.ru/support/tracker/ru/api-ref/issues/get-issue`
- edit issue: `https://yandex.ru/support/tracker/ru/api-ref/issues/patch-issue`
- search issues: `https://yandex.ru/support/tracker/ru/api-ref/issues/search-issues`
- count issues: `https://yandex.ru/support/tracker/ru/api-ref/issues/count-issues`
- move issue: `https://yandex.ru/support/tracker/ru/api-ref/issues/move-issue`
- transitions: `https://yandex.ru/support/tracker/ru/api-ref/issues/get-transitions`
- execute transition: `https://yandex.ru/support/tracker/ru/api-ref/issues/new-transition`
- changelog: `https://yandex.ru/support/tracker/ru/api-ref/issues/get-changelog`
- vote for issue: `https://yandex.ru/support/tracker/ru/api-ref/issues/vote-issue`
- stop voting: `https://yandex.ru/support/tracker/ru/api-ref/issues/stop-vote-issue`
- create report: `https://yandex.ru/support/tracker/ru/api-ref/issues/create-report`

## Issue Filters

Use this area for saved search filters and filter sharing.

- doc family: `Фильтры задач`
- open the family from the API navigation under the overview page when a task needs exact filter methods

## Issue Checklists

Use this area for checklist items stored in issues.

- checklist section root: `https://yandex.ru/support/tracker/ru/api-ref/issues/checklist-items`

## Comments, Checklists, Attachments, Links, Worklog

- add comment: `https://yandex.ru/support/tracker/ru/api-ref/issues/add-comment`
- comments section root: `https://yandex.ru/support/tracker/ru/api-ref/issues/comments`
- attachments section root: `https://yandex.ru/support/tracker/ru/api-ref/issues/attachments`
- download attachment: `https://yandex.ru/support/tracker/ru/api-ref/issues/get-attachment`
- links section root: `https://yandex.ru/support/tracker/ru/api-ref/issues/links`
- worklog section root: `https://yandex.ru/support/tracker/ru/api-ref/issues/issue-worklog`

## Bulk Operations

- bulk changes section root: `https://yandex.ru/support/tracker/ru/api-ref/bulkchange`

Use this area for async mass edits and status checks.

## Fields and Dictionaries

- fields section root: `https://yandex.ru/support/tracker/ru/api-ref/fields`
- field categories family: `категории полей`
- get issue fields: `https://yandex.ru/support/tracker/ru/api-ref/issues/get-issue-fields`
- issue types: `https://yandex.ru/support/tracker/ru/api-ref/admin/get-issue-types`
- statuses: `https://yandex.ru/support/tracker/ru/api-ref/admin/get-statuses`
- resolutions: `https://yandex.ru/support/tracker/ru/api-ref/admin/get-resolutions`
- priorities: `https://yandex.ru/support/tracker/ru/api-ref/admin/get-priorities`

## Queues

Use this area for queue configuration and queue-local schema.

- queues section root: `https://yandex.ru/support/tracker/ru/api-ref/queues`
- get queue: `https://yandex.ru/support/tracker/ru/api-ref/queues/get-queue`
- local fields: `https://yandex.ru/support/tracker/ru/api-ref/queues/get-info-local-field`

## Projects, Portfolios, Goals

Prefer the Entities API for modern planning objects.

- entities overview: `https://yandex.ru/support/tracker/ru/api-ref/entities/about-entities`
- entities section root: `https://yandex.ru/support/tracker/ru/api-ref/entities`

## Projects Legacy

Use this area only when a task explicitly refers to the old projects API.

- doc family: `Проекты (старая версия)`
- open the family from the API navigation under the overview page when a task explicitly references legacy projects

## Automation

Use this area for triggers, actions, auto-rules, and queue automation behavior.

- doc family: `Автоматизация`
- open the family from the API navigation under the overview page when a task needs exact automation methods

## Boards and Dashboards

- boards section root: `https://yandex.ru/support/tracker/ru/api-ref/boards`
- get board: `https://yandex.ru/support/tracker/ru/api-ref/boards/get-board`
- get column: `https://yandex.ru/support/tracker/ru/api-ref/boards/get-column`
- dashboards section root: `https://yandex.ru/support/tracker/ru/api-ref/dashboards`

## Components

Use this area for issue components within queues.

- doc family: `Компоненты`
- open the family from the API navigation under the overview page when a task needs exact component methods

## Time Tracking

Use this area for time tracking and worklog-specific methods.

- worklog section root: `https://yandex.ru/support/tracker/ru/api-ref/issues/issue-worklog`

## Import

Use this area for import jobs and imported issues.

- doc family: `Импорт`
- open the family from the API navigation under the overview page when a task needs exact import methods

## External Application Links

Use this area for links between Tracker objects and external systems.

- doc family: `Связи с внешними приложениями`
- open the family from the API navigation under the overview page when a task needs exact linking methods

## Users

- users section root: `https://yandex.ru/support/tracker/ru/api-ref/users`
- current user info: `https://yandex.ru/support/tracker/ru/api-ref/users/get-user-info`

## Practical Reading Order

Read in this order when implementing a new integration:

1. overview
2. access
3. common format
4. the target resource family
5. error codes

For issue automation, start with Issues, Comments, Attachments, Fields, Queues, and Automation.

## Coverage Note

When a task asks for a function that is not listed here by exact method page, treat the relevant section root as authoritative and look up the precise method there. This reference is a navigation map for the whole docs surface, not a frozen copy of every single article URL.
