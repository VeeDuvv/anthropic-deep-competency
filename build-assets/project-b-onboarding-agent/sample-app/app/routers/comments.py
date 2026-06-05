"""Comment routes for task discussions."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Comment, Project, ProjectMember, Task, User
from app.schemas import CommentCreate, CommentResponse

router = APIRouter(
    prefix="/api/projects/{slug}/tasks/{task_id}/comments",
    tags=["comments"],
)


def _verify_task_access(slug: str, task_id: int, user: User, db: Session) -> Task:
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

    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/", response_model=list[CommentResponse])
def list_comments(
    slug: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = _verify_task_access(slug, task_id, current_user, db)
    return db.query(Comment).filter(Comment.task_id == task.id).order_by(Comment.created_at).all()


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    slug: str,
    task_id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = _verify_task_access(slug, task_id, current_user, db)
    comment = Comment(
        body=comment_in.body,
        task_id=task.id,
        author_id=current_user.id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    slug: str,
    task_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _verify_task_access(slug, task_id, current_user, db)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only the author or admin can delete comments")

    db.delete(comment)
    db.commit()
