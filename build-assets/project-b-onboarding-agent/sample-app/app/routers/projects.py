"""Project CRUD routes with membership management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Project, ProjectMember, User
from app.schemas import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all projects the current user is a member of."""
    project_ids = (
        db.query(ProjectMember.project_id)
        .filter(ProjectMember.user_id == current_user.id)
        .subquery()
    )
    projects = (
        db.query(Project)
        .filter(Project.id.in_(project_ids))
        .filter(Project.is_archived == False)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return projects


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if db.query(Project).filter(Project.slug == project_in.slug).first():
        raise HTTPException(status_code=400, detail="Project slug already exists")

    project = Project(**project_in.model_dump())
    db.add(project)
    db.flush()

    # Creator becomes project owner
    membership = ProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        role="owner",
    )
    db.add(membership)
    db.commit()
    db.refresh(project)
    return project


@router.get("/{slug}", response_model=ProjectResponse)
def get_project(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.slug == slug).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    member = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project.id, ProjectMember.user_id == current_user.id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this project")

    return project


@router.patch("/{slug}", response_model=ProjectResponse)
def update_project(
    slug: str,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.slug == slug).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == current_user.id,
            ProjectMember.role.in_(["owner", "admin"]),
        )
        .first()
    )
    if not member:
        raise HTTPException(status_code=403, detail="Only project owners and admins can update")

    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


@router.post("/{slug}/members", status_code=status.HTTP_201_CREATED)
def add_member(
    slug: str,
    user_id: int,
    role: str = "member",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.slug == slug).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    existing = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project.id, ProjectMember.user_id == user_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="User is already a member")

    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    membership = ProjectMember(project_id=project.id, user_id=user_id, role=role)
    db.add(membership)
    db.commit()
    return {"detail": f"User {target_user.username} added to project {slug}"}
