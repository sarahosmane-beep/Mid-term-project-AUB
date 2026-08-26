# Verification Evidence

## Baseline

The first root-level `python -m pytest` attempt failed during collection before running tests. This workspace contains copied project folders with duplicate `tests` packages plus inaccessible `pytest-cache-files-*` directories. No application assertion failed. I added `pytest.ini` with `testpaths = tests` to target the intended repository suite. The six original tests remained passing after the change.

## Automated tests

- Final command: `python -m pytest -q`
- Result: **12 passed** in 0.56 seconds.
- Seven feature tests cover create/update due dates, invalid date syntax, overdue true/false behavior, title/description search, combined filters, and no matches.
- Existing CRUD, validation, filtering, missing-resource, and health tests remain present.
- Two environment warnings remain: a third-party Starlette/httpx deprecation and inability to create `.pytest_cache`; neither changes test results.

## Manual browser checks

Tested against `http://127.0.0.1:8000/` on 26 August 2026:

1. Created **Release checklist**, High priority, due 25 August 2026. The card displayed `Due Aug 25, 2026` and `Overdue`.
2. Created **Release announcement**, Done, High priority, due 15 September 2026. It displayed the date without an overdue pill.
3. Search `checklist` returned only **Release checklist**.
4. Search `release` + To do + High returned only **Release checklist**.
5. Adding Overdue only still returned only **Release checklist**.
6. Edited the first due date to 27 August 2026. The card persisted the new date and no longer showed Overdue.
7. Browser console inspection found zero errors.

## Behavior contract before and after focused refactor

Before: CRUD, status filtering, priority filtering, 422 validation, and 404 handling passed. Search existed only in the UI and filtered the currently loaded list.

After: all previous behavior still passes; optional due dates round-trip through create/update; overdue excludes completed work; and `q`, status, priority, assignee, and overdue compose on the server. The focused refactor moved search request handling behind a 250 ms debounce. The full 12-test contract passed afterward.

## Break Tests

1. **Overdue assertion:** Temporarily changed the expected overdue title from `Late open task` to `Incorrect task`. The targeted test failed with actual `['Late open task']`, proving it detects wrong overdue results. The correct assertion was restored.
2. **Search input:** Temporarily changed the title-search query from `launch` to `missing` while retaining the expected task. The targeted test failed with actual `[]`, proving it detects broken search matching. The correct query was restored.

The full suite was rerun after both restorations.
