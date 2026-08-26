from datetime import date, datetime, timezone
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskFields(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: str | None = Field(default=None, max_length=100)
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def title_must_contain_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must contain non-whitespace characters")
        return value


class TaskCreate(TaskFields):
    pass


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee: str | None = Field(default=None, max_length=100)
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def updated_title_must_contain_text(cls, value: str | None) -> str:
        if value is None or not value.strip():
            raise ValueError("title must contain non-whitespace characters")
        return value.strip()

    @field_validator("status", "priority")
    @classmethod
    def required_fields_cannot_be_cleared(cls, value: object) -> object:
        if value is None:
            raise ValueError("field cannot be null")
        return value


class Task(TaskFields):
    id: int
    created_at: datetime
    updated_at: datetime


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
