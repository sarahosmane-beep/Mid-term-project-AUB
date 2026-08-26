# Mid-Course Project Submission Guide

## GitHub submission link

**Submit this link:** [Mid-term Project — `mid-course-project` branch](https://github.com/sarahosmane-beep/Mid-term-project-AUB/tree/mid-course-project)

Checkpoint commit: `986afb6` — `Complete mid-course feature extension sprint`

## Deliverables checklist

| Required deliverable | Location in this folder | What it contains |
|---|---|---|
| Updated backend source code | `app/` | FastAPI application, task models, routes, and in-memory storage with due dates, overdue filtering, search, and combined filters. |
| Updated frontend source code | `task-tracker.html` and `app.js` | Due-date input, due-date and overdue card indicators, overdue selector, and API-backed search/filter controls. |
| Existing and new pytest tests | `tests/` | Existing health and task behavior tests plus seven new feature tests. Final result: 12 tests passed. |
| User stories | `docs/midcourse/user-stories.md` | Three to five stories per feature, acceptance criteria, and one corrected AI assumption per feature. |
| Mini architecture decision record | `docs/midcourse/mini-adr.md` | Selected implementation, alternatives suggested by AI, and options rejected as too complex or out of scope. |
| AI prompt log | `docs/midcourse/prompt-log.md` | At least three meaningful prompts per feature, including a weak prompt rewritten more precisely and accept/edit/reject decisions. |
| Verification evidence | `docs/midcourse/verification.md` | Baseline findings, automated test results, manual browser checks, behavior contract, and two Break Tests. |
| Reflection | `docs/midcourse/reflection.md` | A 335-word reflection covering AI tools, where AI helped and slowed progress, and where review changed the result. |
| Run and test instructions | `README.md` | Environment setup, backend startup, frontend URL, test command, features, and API endpoints. |
| Python dependencies | `requirements.txt` | FastAPI, Uvicorn, HTTPX, and pytest requirements. |
| Test discovery configuration | `pytest.ini` | Limits test discovery to the intended root `tests/` folder. |
| Environment example and exclusions | `.env.example` and `.gitignore` | Safe environment placeholder and rules excluding secrets, caches, virtual environments, and editor files. |
| Earlier architecture context | `docs/adr/0001-initial-architecture.md` | Original Task Tracker architecture decision record retained for context. |

## Features completed

### Feature 1: Due dates and overdue filtering

- Optional due dates are accepted during task creation and updates.
- Invalid date formats receive HTTP 422 validation responses.
- Open tasks due before today are marked overdue.
- Completed tasks are excluded from overdue results.
- The frontend displays due dates and an overdue pill and provides an overdue filter.

### Feature 2: Search and combined filters

- `GET /tasks?q=...` searches task titles and descriptions without case sensitivity.
- Search combines with status, priority, assignee, and overdue filters using AND behavior.
- No-match searches return HTTP 200 with an empty list.
- The frontend sends debounced search requests while keeping all filter controls visible.

## Verification summary

- Full automated suite: **12 passed**.
- Six pre-existing tests remained passing.
- Seven new feature tests were added.
- Manual browser checks covered creation, editing, due-date display, overdue display, search, and combined filters.
- Browser console errors found: **0**.
- Two Break Tests were performed and documented.

## How to run the submission

From this folder:

```powershell
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://localhost:8000/> in a browser.

Run the tests with:

```powershell
python -m pytest
```

## Submission note

The required branch is named `mid-course-project`. The folder contains no credentials, private data, Git metadata, caches, copied projects, or unrelated generated archives.
