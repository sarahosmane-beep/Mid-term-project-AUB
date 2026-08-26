import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.storage.task_store import task_store


client = TestClient(app)


@pytest.fixture(autouse=True)
def empty_store() -> None:
    task_store.clear()


def create_task(**overrides: str) -> dict:
    payload = {
        "title": "Write documentation",
        "description": "Cover the public API",
        "status": "ToDo",
        "priority": "High",
        "assignee": "Sam",
        **overrides,
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_and_get_task() -> None:
    created = create_task()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Write documentation"
    assert response.json()["created_at"]


def test_list_tasks_can_filter_status_and_priority() -> None:
    create_task()
    create_task(title="Ship release", status="Done", priority="Low")
    assert len(client.get("/tasks").json()) == 2
    filtered = client.get("/tasks", params={"status": "Done", "priority": "Low"})
    assert [task["title"] for task in filtered.json()] == ["Ship release"]


def test_update_task_including_status_transition() -> None:
    created = create_task()
    response = client.patch(
        f"/tasks/{created['id']}",
        json={"status": "InProgress", "assignee": "Jo"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"
    assert response.json()["assignee"] == "Jo"


def test_delete_task() -> None:
    created = create_task()
    assert client.delete(f"/tasks/{created['id']}").status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_validation_and_missing_tasks() -> None:
    assert client.post("/tasks", json={"title": ""}).status_code == 422
    assert client.patch("/tasks/999", json={"status": "Done"}).status_code == 404
    assert client.delete("/tasks/999").status_code == 404


def test_due_date_can_be_created_and_updated() -> None:
    created = create_task(due_date="2026-09-15")
    assert created["due_date"] == "2026-09-15"

    response = client.patch(f"/tasks/{created['id']}", json={"due_date": "2026-10-01"})
    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-10-01"


def test_invalid_due_date_is_rejected() -> None:
    response = client.post("/tasks", json={"title": "Bad date", "due_date": "next Friday"})
    assert response.status_code == 422


def test_overdue_filter_excludes_completed_and_future_tasks() -> None:
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    create_task(title="Late open task", due_date=yesterday)
    create_task(title="Late completed task", due_date=yesterday, status="Done")
    create_task(title="Future task", due_date=tomorrow)
    create_task(title="No deadline")

    overdue = client.get("/tasks", params={"overdue": "true"})
    assert overdue.status_code == 200
    assert [task["title"] for task in overdue.json()] == ["Late open task"]

    not_overdue = client.get("/tasks", params={"overdue": "false"})
    assert {task["title"] for task in not_overdue.json()} == {
        "Late completed task", "Future task", "No deadline"
    }


def test_search_matches_title_and_description_case_insensitively() -> None:
    create_task(title="Prepare Launch", description="Coordinate release notes")
    create_task(title="Review budget", description="Finance planning")

    title_match = client.get("/tasks", params={"q": "launch"})
    description_match = client.get("/tasks", params={"q": "RELEASE"})
    assert [task["title"] for task in title_match.json()] == ["Prepare Launch"]
    assert [task["title"] for task in description_match.json()] == ["Prepare Launch"]


def test_search_combines_with_status_and_priority_filters() -> None:
    create_task(title="Release checklist", status="ToDo", priority="High")
    create_task(title="Release announcement", status="Done", priority="High")
    create_task(title="Release notes", status="ToDo", priority="Low")

    response = client.get(
        "/tasks", params={"q": "release", "status": "ToDo", "priority": "High"}
    )
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Release checklist"]


def test_search_with_no_matches_returns_empty_list() -> None:
    create_task()
    response = client.get("/tasks", params={"q": "no-such-task"})
    assert response.status_code == 200
    assert response.json() == []
