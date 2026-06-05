"""Task CRUD routes with filtering, assignment, and status transitions."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Project, ProjectMember, Task, TaskPriority, TaskStatus, User
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/projects/{slug}/tasks", tags=["tasks"])


def _get_project_for_member(slug: str, user: User, db: Session) -> Project:
    """Helper: get project and verify user membership."""
    project = db.query(Project).filter(Project.slug == slug).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    member = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project.id, ProjectMember.user_id == user.id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this project")

    return project


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    slug: str,
    status_filter: TaskStatus | None = Query(None, alias="status"),
    priority_filter: TaskPriority | None = Query(None, alias="priority"),
    assignee_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = _get_project_for_member(slug, current_user, db)
    query = db.query(Task).filter(Task.project_id == project.id)

    if status_filter:
        query = query.filter(Task.status == status_filter)
    if priority_filter:
        query = query.filter(Task.priority == priority_filter)
    if assignee_id is not None:
        query = query.filter(Task.assignee_id == assignee_id)

    return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    slug: str,
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = _get_project_for_member(slug, current_user, db)

    if task_in.assignee_id:
        assignee_member = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == task_in.assignee_id,
            )
            .first()
        )
        if not assignee_member:
            raise HTTPException(status_code=400, detail="Assignee is not a project member")

    task = Task(
        **task_in.model_dump(),
        project_id=project.id,
        creator_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    slug: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = _get_project_for_member(slug, current_user, db)
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    slug: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = _get_project_for_member(slug, current_user, db)
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)

    # Track completion timestamp
    if "status" in update_data:
        new_status = update_data["status"]
        if new_status == TaskStatus.DONE and task.status != TaskStatus.DONE:
            task.completed_at = datetime.now(timezone.utc)
        elif new_status != TaskStatus.DONE:
            task.completed_at = None

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    slug: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = _get_project_for_member(slug, current_user, db)
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only the creator or admin can delete tasks")

    db.delete(task)
    db.commit()
