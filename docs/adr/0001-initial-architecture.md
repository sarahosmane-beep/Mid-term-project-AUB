# ADR 0001: Initial Task Tracker architecture

- Status: Accepted
- Date: 2026-08-15

## Context

This is a small FastAPI learning project. It will eventually provide CRUD operations
for tasks with `id`, `title`, `description`, `status`, `priority`, and `assignee`.
The first module needs only a runnable, testable skeleton.

## Decision

- Organize code under `app/`, separating routes, core concerns, models, and storage.
- Use FastAPI with Uvicorn.
- Expose `GET /health` as the only application endpoint in the initial scaffold.
- Return a UTC ISO 8601 timestamp from the health endpoint.
- Reserve `app/storage/` for a later in-memory repository.
- Keep tests under `tests/` and use FastAPI's `TestClient` with pytest.

## Deferred

- Task CRUD endpoints and business rules
- Authentication and user accounts
- Production databases and persistence
- Docker, cloud deployment, and microservices

## Consequences

The application can be installed, started, and checked immediately while leaving
task behavior to a later requirements-driven implementation step.
