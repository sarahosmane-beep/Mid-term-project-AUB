# Mini-ADR: Due dates and server-side search

**Status:** Accepted — 26 August 2026

## Context

Taskflow already supported task CRUD plus status and priority filtering. The sprint needed two small end-to-end features with visible frontend behavior and backend tests.

## Decision

Store `due_date` as Pydantic's `date | None` on the existing in-memory task model. Compute overdue status when listing tasks: a task is overdue only when it has a date before today and is not `Done`. Expose this through the optional `overdue` boolean query parameter. The UI renders the date and an overdue pill and supplies an overdue selector.

Move text search to `GET /tasks?q=...`. Search uses case-insensitive substring matching over title and description and composes with status, priority, assignee, and overdue filters using AND semantics. The UI sends debounced search requests rather than filtering a partial client-side result.

## Alternatives considered

AI suggested adding a persisted `is_overdue` field, but that value becomes stale as time passes, so it was rejected. A database migration and timezone-configurable deadlines were rejected as out of scope for an in-memory course app. AI also suggested a general query language and fuzzy search; both would add complexity without supporting the acceptance criteria. Searching assignees inside `q` was rejected to keep the contract explicit; an exact `assignee` filter is supported separately.

## Consequences

Dates use the simple ISO calendar-date contract and contain no time-of-day. Overdue results remain current without background jobs. Server-side search gives API and UI users identical behavior. Statistics currently describe the loaded/filter result set, which is consistent with the existing frontend architecture.
