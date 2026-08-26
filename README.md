# Task Tracker API

A complete, compact FastAPI task tracker with a browser frontend.

## Requirements

- Python 3.10 or newer

## Setup

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Then verify the service:

```bash
curl http://localhost:8000/health
```

Expected shape:

```json
{"status":"ok","timestamp":"2026-08-15T12:00:00+00:00"}
```

Interactive API documentation is available at <http://localhost:8000/docs>.
The task tracker is available at <http://localhost:8000/>.

## Test

```bash
python -m pytest
```

## Features

Included:

- Create, view, edit, transition, and delete tasks
- Add optional due dates and identify or filter overdue work
- Search task titles and descriptions, combined with status and priority filters
- Validated status (`ToDo`, `InProgress`, `Done`) and priority (`Low`, `Medium`, `High`)
- Responsive web interface backed by the API
- In-memory, thread-safe storage (data resets when the process restarts)
- Health check and interactive OpenAPI documentation

## API

- `POST /tasks`
- `GET /tasks?status=ToDo&priority=High&q=release&overdue=true`
- `GET /tasks/{id}`
- `PATCH /tasks/{id}`
- `DELETE /tasks/{id}`
