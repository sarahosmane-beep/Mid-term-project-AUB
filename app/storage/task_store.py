from threading import Lock

from app.models.task import Task, TaskCreate, TaskUpdate, now_utc


class TaskStore:
    """Small thread-safe in-memory store suitable for this single-process app."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1
        self._lock = Lock()

    def list(self) -> list[Task]:
        with self._lock:
            return [task.model_copy() for task in reversed(self._tasks.values())]

    def get(self, task_id: int) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            return task.model_copy() if task else None

    def create(self, data: TaskCreate) -> Task:
        with self._lock:
            timestamp = now_utc()
            task = Task(
                id=self._next_id,
                created_at=timestamp,
                updated_at=timestamp,
                **data.model_dump(),
            )
            self._tasks[task.id] = task
            self._next_id += 1
            return task.model_copy()

    def update(self, task_id: int, data: TaskUpdate) -> Task | None:
        with self._lock:
            current = self._tasks.get(task_id)
            if current is None:
                return None
            changes = data.model_dump(exclude_unset=True)
            updated = current.model_copy(update={**changes, "updated_at": now_utc()})
            self._tasks[task_id] = updated
            return updated.model_copy()

    def delete(self, task_id: int) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._tasks.clear()
            self._next_id = 1


task_store = TaskStore()
