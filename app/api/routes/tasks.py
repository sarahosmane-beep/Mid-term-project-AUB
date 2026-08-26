from datetime import date

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.models.task import Task, TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.storage.task_store import task_store


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate) -> Task:
    return task_store.create(data)


@router.get("", response_model=list[Task])
def list_tasks(
    task_status: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = None,
    q: str | None = Query(default=None, max_length=100),
    assignee: str | None = Query(default=None, max_length=100),
    overdue: bool | None = None,
) -> list[Task]:
    tasks = task_store.list()
    if task_status is not None:
        tasks = [task for task in tasks if task.status == task_status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if q is not None and q.strip():
        needle = q.strip().casefold()
        tasks = [
            task
            for task in tasks
            if needle in task.title.casefold()
            or needle in (task.description or "").casefold()
        ]
    if assignee is not None:
        needle = assignee.strip().casefold()
        tasks = [task for task in tasks if (task.assignee or "").casefold() == needle]
    if overdue is not None:
        today = date.today()
        tasks = [
            task
            for task in tasks
            if (task.due_date is not None and task.due_date < today and task.status != TaskStatus.DONE)
            is overdue
        ]
    return tasks


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = task_store.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate) -> Task:
    task = task_store.update(task_id, data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    if not task_store.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
