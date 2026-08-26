# Repository Guardrails

## Read first

Before changing code, read `README.md`, the relevant source and tests, and the evidence documents in `docs/`. Prefer documentation and tests that describe current behavior over assumptions.

## Stack and commands

- Backend: Python 3.12, FastAPI, Pydantic, Uvicorn.
- Frontend: static HTML, CSS, and JavaScript in `frontend/`.
- Install: `python -m pip install -r requirements.txt`.
- Run: `python -m uvicorn app.main:app --reload`.
- Test: `python -m pytest -q`.
- Docker: `docker build -t task-tracker-final .`.

## Project rules

- Preserve the course scope: no authentication, comments, notifications, production database, or unrelated UI work.
- Preserve the completed mid-course behavior: due dates, overdue filtering, text search, assignee filtering, combined filters, and the evidence under `docs/midcourse/`.
- Treat `app/` and `frontend/` as protected. Change them only for a small verified bug/security fix or a documentation-supported correction, and explain the change in `docs/final-ai-review.md`.
- Add or update tests when behavior changes. Run the full suite before submission.
- Never commit `.env`, credentials, tokens, production logs, or personal/customer data.
- Inspect every AI-generated diff. Do not keep a line, command, or configuration choice that you cannot explain.
- Record material AI review decisions, including rejected or corrected suggestions, in `docs/final-ai-review.md`.
