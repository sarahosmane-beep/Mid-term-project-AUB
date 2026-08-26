# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes.
- Docs-first/read-first guardrail included: yes.
- Unexpected `app/`/`frontend/` edits rule included: yes.
- Scope, secrets, verification, and ownership rules included: yes.

## AI code review mini-log

Reviewed file: `Dockerfile`.

| AI comment | Grade | Reason | Verification or decision |
|---|---|---|---|
| Run the service as a non-root user. | Useful | It reduces the effect of a container compromise without changing app behavior. | Kept `USER appuser`; verified it appears after file copies and before `CMD`. |
| Add a Docker `HEALTHCHECK` instruction. | Noise | The assignment requires an external `/health` verification, and a built-in health check would require adding another runtime utility or a longer Python command. | Rejected; kept the runtime image small and documented the external curl check. |
| Copy the entire repository with `COPY . .` for simplicity. | Wrong | That broad copy can include tests, docs, local files, or secrets if ignore rules regress. | Replaced with narrow copies of `requirements.txt`, `app/`, and `frontend/`. |

## AI security mini-review

| Finding | File evidence | Grade | Reason | Next action |
|---|---|---|---|---|
| The API has no authentication. | `app/main.py`, `app/api/routes/tasks.py` | Valid | Anyone who can reach the service can modify in-memory tasks. Authentication is explicitly out of scope for this course release. | Keep the demo bound to trusted/local environments; do not present it as a production multi-user service. |
| Rendering task data with `innerHTML` may allow stored XSS. | `frontend/app.js` (`render`, `escapeHtml`) | False Positive | User-controlled title, description, and assignee are passed through `escapeHtml`; status, priority, and numeric ID are server-validated/normalized values. | Preserve escaping and re-review if new interpolated fields are added. |
| Dependency ranges are not fully locked. | `requirements.txt` | Valid | Rebuilds can resolve newer compatible releases, which weakens reproducibility compared with a lock file. | Accept for this small course project; use automated updates and a reviewed lock strategy before production use. |
| `--reload` exposes a development reloader in production. | `README.md`, `Dockerfile` | False Positive | Reload is only in the local-development command; the container `CMD` does not use it. | Keep the commands clearly separated. |

## Manual security check

I manually traced every Docker build input and confirmed that the Dockerfile does not use `COPY . .`. Only the dependency list, backend, and frontend enter the image, while `.env` patterns are excluded. I also searched the submitted files for credential-like names and found no real secret values. This matters because an otherwise correct application can still leak credentials through its build context or image layers.

## One AI output I rejected or corrected

AI suggested adding authentication after identifying the unauthenticated task endpoints. I rejected that implementation because the project brief explicitly forbids authentication as a new feature, and adding it at release time would create larger correctness and security risks. I kept the finding, documented the deployment limitation, and left the product scope unchanged. I also rejected an earlier packaging approach that used a new repository and an older app snapshot; the corrected final branch now starts from the actual mid-course history and preserves due dates, search, overdue filtering, and their tests.

## Three AI usage rules

1. Never paste credentials, `.env` values, tokens, production logs, or personal/customer data into an AI tool.
2. Always verify AI output by reading the diff and running the smallest relevant check followed by the full test suite; verify runtime claims against the running service when possible.
3. Record material AI contributions by naming the file or decision, grading important findings, and noting what was corrected or rejected.

## Ownership statement

I am comfortable submitting this repository because I reviewed the project history, structure, commands, configurations, and evidence rather than accepting generated output blindly. The final branch is based on the completed mid-course branch, and the established application behavior and tests are preserved. I ran all 12 tests, checked the API and frontend, built and ran the Docker image, and confirmed the container used the non-root `appuser`. GitHub CI evidence is recorded only after the hosted workflow completes.
