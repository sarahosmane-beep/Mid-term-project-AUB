# Release Evidence

## Baseline

- Repository: https://github.com/sarahosmane-beep/Mid-term-project-AUB
- Branch: `final-project`, created from the completed `mid-course-project` history.
- Verification date: 2026-08-26.
- Local app run command: `python -m uvicorn app.main:app --reload`.
- `/health` result: HTTP 200 with `status: ok` and a timezone-aware timestamp.
- Frontend check: `/` and `/app.js` returned HTTP 200. The create/edit flow, due-date field, search, status/priority filters, and overdue filter remain visible.
- Mid-course scope check: due dates, overdue filtering, text search, assignee filtering, combined filters, and all earlier evidence under `docs/midcourse/` are preserved.
- Test command: `python -m pytest -q`.
- Test result: 12 passed in 1.55 seconds. A dependency deprecation warning from the installed FastAPI test client did not affect the tests.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`.
- Workflow triggers: push, pull request, and manual dispatch.
- Test command used by CI: `python -m pytest -q`.
- Dependency setup: explicit Python 3.12 with `python -m pip install -r requirements.txt`.
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.
- Verified green run: https://github.com/sarahosmane-beep/Mid-term-project-AUB/actions/runs/33002670773 (all steps passed in 11 seconds on 2026-08-26).

## Docker evidence

- Build command: `docker build -t task-tracker-final-midcourse .`.
- Run command: `docker run --rm -p 8000:8000 --name task-tracker-final-corrected task-tracker-final-midcourse`.
- Build result: successful with Docker Engine 29.3.1 and Docker Desktop 4.66.1 on 2026-08-26.
- `/health` check: HTTP 200 with `{"status":"ok","timestamp":"2026-08-26T18:56:18.822868+00:00"}`.
- Frontend check: HTTP 200; the rendered HTML contained the preserved Due date field.
- Non-root check: `docker exec task-tracker-final-corrected whoami` returned `appuser`.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`; the Dockerfile copies only `requirements.txt`, `app/`, and `frontend/`.
- Runtime command check: explicit Uvicorn command binds `0.0.0.0:8000`.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The final work uses the same repository and preserves the mid-course history | Git remote, branch history, and `docs/midcourse/` | Pass | Created `final-project` from `mid-course-project` in `Mid-term-project-AUB` |
| `python -m pytest -q` runs the complete preserved suite | Ran the command from the repository root | Pass: 12 tests | Disabled only pytest's cache provider to avoid workspace cache-permission noise; test discovery and assertions are unchanged |
| Due dates, overdue filtering, and search remain functional | Existing tests plus API and frontend checks | Pass | No feature removal; copied the established frontend into the required `frontend/` directory |
| `GET /health` returns HTTP 200 and `status: ok` | Local TestClient and running Docker container | Pass | None |
| Docker runs as a non-root user without copying `.env` | Successful build/run, `whoami`, Dockerfile, `.dockerignore` | Pass | Added explicit `USER appuser` and narrow `COPY` commands |
| CI installs dependencies and runs pytest without shortcuts | Workflow inspection and hosted run | Pass: 12 tests in GitHub Actions | Added explicit Python, installation, and pytest steps |

## Submission

- Submit the public repository URL: https://github.com/sarahosmane-beep/Mid-term-project-AUB
- Keep both `mid-course-project` and `final-project` branches available.
