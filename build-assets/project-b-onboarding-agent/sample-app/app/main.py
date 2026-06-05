"""TaskFlow API — A project management API built with FastAPI.

This is the main application entry point. It configures middleware,
includes all routers, and creates database tables on startup.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, comments, projects, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="A project management API with tasks, comments, and team collaboration.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(comments.router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.app_name}


@app.get("/api/stats")
def get_stats():
    """Return basic application statistics."""
    from sqlalchemy import func

    from app.database import SessionLocal
    from app.models import Project, Task, User

    db = SessionLocal()
    try:
        return {
            "users": db.query(func.count(User.id)).scalar(),
            "projects": db.query(func.count(Project.id)).scalar(),
            "tasks": db.query(func.count(Task.id)).scalar(),
        }
    finally:
        db.close()
