# User Stories

## Feature 1: Due dates and overdue filtering

1. As a task owner, I want to add an optional due date so that I know when work is expected.
   - A task can be created with an ISO date (`YYYY-MM-DD`) or no date.
   - Invalid dates receive HTTP 422 and are not stored.
2. As a task owner, I want to change a due date while editing so that plans can change.
   - Editing pre-fills the existing date.
   - Saving a new date persists it without changing unrelated fields.
3. As a user, I want overdue work highlighted so that urgent work is obvious.
   - An open task is overdue when its due date is before the current local date.
   - Completed tasks never display as overdue.
4. As a user, I want to filter overdue work so that I can focus on missed deadlines.
   - `overdue=true` returns only open tasks whose dates are in the past.
   - `overdue=false` includes future, undated, and completed tasks.

**AI assumption corrected:** The first design treated every past-due task as overdue. I corrected it so completed tasks are not overdue, matching normal task-tracker expectations.

## Feature 2: Search and combined filters

1. As a user, I want to search titles and descriptions so that I can find a task from remembered words.
   - Search is case-insensitive and ignores leading/trailing whitespace.
   - No match returns HTTP 200 with an empty list.
2. As a user, I want search to combine with status and priority so that I can narrow a large board.
   - All supplied filters use AND semantics.
   - Valid combinations return only tasks satisfying every condition.
3. As an API consumer, I want invalid enum filters rejected so that mistakes are visible.
   - Invalid status or priority values receive HTTP 422.
4. As a browser user, I want search results to update without a submit button so that filtering feels immediate.
   - Input is debounced briefly before requesting the API.
   - Empty results keep the task panel and filter controls visible.

**AI assumption corrected:** The existing frontend searched assignee text too. I limited the new API search contract to title and description because that is the scoped feature in the brief; assignee remains a separate exact-match API filter.
