# Prompt Log

The entries below summarize the meaningful instructions used during the AI-assisted sprint. Large transcripts are intentionally omitted.

## Feature 1: Due dates and overdue filtering

### Prompt 1 — planning and constraints

> Inspect the existing Pydantic task model, routes, store, frontend form, and tests. Propose the smallest end-to-end due-date design. Keep storage in memory and avoid database or timezone infrastructure.

AI proposed `date | None`, create/update support, a computed overdue filter, and UI date/pill controls. I accepted the model shape and rejected a stored `is_overdue` flag because it would become stale.

### Prompt 2 — implementation

> Add optional ISO due dates to create and patch. Define overdue as due before today and status not Done. Add `overdue=true|false`, a date input, card date, overdue pill, and filter selector. Preserve all existing fields and endpoints.

AI returned focused model, route, HTML, and JavaScript changes. I edited the browser calculation to use a local `YYYY-MM-DD` value rather than comparing UTC timestamps, preventing date-boundary surprises.

### Prompt 3 — tests and review

> Add tests for valid create/update dates, invalid date format, overdue inclusion, and exclusion of completed/future/undated tasks. Use dates relative to today so tests do not expire.

AI supplied dynamic-date tests. I accepted them after checking that both `overdue=true` and `overdue=false` were covered.

## Feature 2: Search and combined filters

### Prompt 1 — weak prompt and rewrite

Weak prompt:

> Add search.

Stronger rewrite:

> Extend `GET /tasks` with optional `q` search over title and description, case-insensitive substring matching, maximum 100 characters, and AND composition with status and priority. Return 200/[] for no matches and leave invalid enums to FastAPI's 422 validation. Connect the existing search box with a short debounce.

The weak prompt left fields, matching rules, validation, and UI behavior ambiguous. I accepted the stronger contract and rejected fuzzy matching as out of scope.

### Prompt 2 — implementation inspection

> Review the filter pipeline for partial-result bugs. Ensure the frontend sends every active filter to the API and does not apply search only to tasks already fetched under stale filters.

AI identified that client-side search and server-side enum filters created two behavior layers. I accepted moving search to the API and edited event handling to debounce text input while loading immediately for selects.

### Prompt 3 — tests and browser verification

> Test title and description search, case insensitivity, combined q+status+priority, and empty results. Then manually create two tasks and verify search, combined filters, empty states, and console errors in the browser.

AI generated focused pytest cases and a browser checklist. I accepted the cases, then manually verified the rendered cards and inspected browser errors rather than trusting the code alone.
