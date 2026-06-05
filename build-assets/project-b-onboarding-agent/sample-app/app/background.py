"""Background tasks using Celery for async processing.

Tasks include sending notification emails, generating project reports,
and cleaning up archived data.
"""

from datetime import datetime, timedelta, timezone

from celery import Celery

from app.config import settings

celery_app = Celery("taskflow", broker=settings.redis_url, backend=settings.redis_url)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "cleanup-archived-tasks": {
            "task": "app.background.cleanup_archived_tasks",
            "schedule": timedelta(hours=24),
        },
        "generate-daily-digest": {
            "task": "app.background.send_daily_digest",
            "schedule": timedelta(hours=24),
        },
    },
)


@celery_app.task
def send_task_notification(user_email: str, task_title: str, action: str):
    """Send email notification when a task is assigned, updated, or completed.

    In production, this would integrate with SendGrid, SES, or similar.
    For now, we just log the notification.
    """
    print(f"[NOTIFICATION] To: {user_email} | Task: {task_title} | Action: {action}")
    return {"status": "sent", "to": user_email, "task": task_title, "action": action}


@celery_app.task
def generate_project_report(project_id: int):
    """Generate a summary report for a project.

    Counts tasks by status, calculates completion rate,
    and identifies overdue tasks.
    """
    from app.database import SessionLocal
    from app.models import Task, TaskStatus

    db = SessionLocal()
    try:
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        total = len(tasks)
        if total == 0:
            return {"project_id": project_id, "total": 0, "message": "No tasks found"}

        by_status = {}
        overdue = 0
        now = datetime.now(timezone.utc)

        for task in tasks:
            status_val = task.status.value if hasattr(task.status, "value") else task.status
            by_status[status_val] = by_status.get(status_val, 0) + 1
            if task.due_date and task.due_date < now and task.status != TaskStatus.DONE:
                overdue += 1

        done_count = by_status.get("done", 0)
        completion_rate = round(done_count / total * 100, 1)

        report = {
            "project_id": project_id,
            "total_tasks": total,
            "by_status": by_status,
            "completion_rate": completion_rate,
            "overdue_tasks": overdue,
            "generated_at": now.isoformat(),
        }
        print(f"[REPORT] Project {project_id}: {completion_rate}% complete, {overdue} overdue")
        return report
    finally:
        db.close()


@celery_app.task
def cleanup_archived_tasks():
    """Delete tasks that have been archived for more than 90 days."""
    from app.database import SessionLocal
    from app.models import Task, TaskStatus

    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=90)
        old_tasks = (
            db.query(Task)
            .filter(Task.status == TaskStatus.ARCHIVED, Task.updated_at < cutoff)
            .all()
        )
        count = len(old_tasks)
        for task in old_tasks:
            db.delete(task)
        db.commit()
        print(f"[CLEANUP] Deleted {count} archived tasks older than 90 days")
        return {"deleted": count}
    finally:
        db.close()


@celery_app.task
def send_daily_digest():
    """Send a daily digest email to all users with their active tasks."""
    from app.database import SessionLocal
    from app.models import Task, TaskStatus, User

    db = SessionLocal()
    try:
        active_users = db.query(User).filter(User.is_active == True).all()
        digests_sent = 0

        for user in active_users:
            active_tasks = (
                db.query(Task)
                .filter(
                    Task.assignee_id == user.id,
                    Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS]),
                )
                .all()
            )
            if active_tasks:
                print(
                    f"[DIGEST] To: {user.email} | {len(active_tasks)} active tasks"
                )
                digests_sent += 1

        return {"digests_sent": digests_sent}
    finally:
        db.close()
