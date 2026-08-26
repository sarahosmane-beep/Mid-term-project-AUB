# Task Tracker API

A compact FastAPI task tracker with a browser-based Kanban interface. Data is stored in memory and resets when the process stops.

## Requirements

- Python 3.12 or newer
- Docker Desktop for the container workflow

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The mid-course Task Tracker and its established features remain intact.
- Due dates, overdue filtering, text search, assignee filtering, and combined filters are preserved.
- CI runs the complete pytest suite on push, pull request, or manual dispatch.
- The Docker image runs as a non-root user and exposes a healthy API on port 8000.
- AI review, security, verification, and ownership evidence is recorded in `docs/`.

### How to run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

On macOS or Linux, activate with `source .venv/bin/activate`. Open <http://127.0.0.1:8000/> for the Taskflow board or <http://127.0.0.1:8000/docs> for API documentation. Verify health with:

```bash
curl -i http://127.0.0.1:8000/health
```

### How to run tests

```bash
python -m pytest -q
```

### How to run with Docker

```bash
docker build -t task-tracker-final .
docker run --rm -p 8000:8000 --name task-tracker-final task-tracker-final
curl -i http://127.0.0.1:8000/health
```

Stop the foreground container with Ctrl+C.

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`
- `docs/midcourse/` (preserved mid-course evidence)

### AI assistance summary

AI helped review the brief, draft CI and Docker configuration, review security, and organize the release evidence. I verified the work by inspecting the diff, running all tests, checking the API and frontend routes, building and running Docker, confirming the non-root runtime user, and reviewing GitHub Actions. I rejected adding authentication because it would violate the explicit final-project scope.

## Features

- Create, view, edit, transition, and delete tasks
- Add optional due dates and identify or filter overdue work
- Search task titles and descriptions
- Filter by status, priority, assignee, and overdue state
- Combine search with status and priority filters
- Responsive frontend backed by the API
- In-memory, thread-safe storage
- Health check and interactive OpenAPI documentation

## API

- `POST /tasks`
- `GET /tasks?status=ToDo&priority=High&q=release&assignee=Sam&overdue=true`
- `GET /tasks/{id}`
- `PATCH /tasks/{id}`
- `DELETE /tasks/{id}`
