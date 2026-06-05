"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models import TaskPriority, TaskStatus


# --- Auth ---


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


# --- Users ---


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8)
    full_name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str | None
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None


# --- Projects ---


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    slug: str = Field(min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    slug: str
    is_archived: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_archived: bool | None = None


# --- Tasks ---


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: int | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    project_id: int
    creator_id: int
    assignee_id: int | None
    due_date: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: int | None = None
    due_date: datetime | None = None


# --- Comments ---


class CommentCreate(BaseModel):
    body: str = Field(min_length=1)


class CommentResponse(BaseModel):
    id: int
    body: str
    task_id: int
    author_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
