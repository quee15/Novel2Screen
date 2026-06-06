from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Task, Project
from schemas import TaskResponse
from exceptions import NotFoundError, BadRequestError

router = APIRouter()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundError("Task")
    return task


@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise NotFoundError("Project")
    return db.query(Task).filter(Task.project_id == project_id).order_by(Task.created_at.desc()).all()


@router.post("/tasks/{task_id}/cancel", response_model=TaskResponse)
def cancel_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundError("Task")
    if task.status in ("succeeded", "failed", "canceled"):
        raise BadRequestError("Cannot cancel a completed task")
    task.status = "canceled"
    task.message = "任务已取消"
    db.commit()
    db.refresh(task)
    return task
