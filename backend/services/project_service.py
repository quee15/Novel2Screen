from sqlalchemy.orm import Session
from models import Project
from schemas import ProjectCreate, ProjectUpdate
from utils import generate_id
from exceptions import NotFoundError
from logger import logger


class ProjectService:
    @staticmethod
    def create(db: Session, data: ProjectCreate) -> Project:
        project = Project(
            id=generate_id("project"),
            title=data.title,
            description=data.description,
            creator=data.creator,
            status="draft",
            schema_version="1.0",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        logger.info(f"Project created: {project.id}")
        return project

    @staticmethod
    def get_all(db: Session) -> list[Project]:
        return db.query(Project).all()

    @staticmethod
    def get_by_id(db: Session, project_id: str) -> Project:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project")
        return project

    @staticmethod
    def update(db: Session, project_id: str, data: ProjectUpdate) -> Project:
        project = ProjectService.get_by_id(db, project_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        db.commit()
        db.refresh(project)
        logger.info(f"Project updated: {project_id}")
        return project
