from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import DocumentResponse, ChapterResponse, ChapterDetailResponse
from services.upload_service import UploadService
from models import SourceDocument, Chapter
from exceptions import NotFoundError

router = APIRouter()


@router.post("/projects/{project_id}/source")
async def upload_source(project_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return UploadService.upload(db, project_id, file)


@router.get("/projects/{project_id}/chapters", response_model=List[ChapterResponse])
def get_chapters(project_id: str, db: Session = Depends(get_db)):
    chapters = db.query(Chapter).filter(Chapter.project_id == project_id).order_by(Chapter.index).all()
    return chapters


@router.get("/chapters/{chapter_id}", response_model=ChapterDetailResponse)
def get_chapter(chapter_id: str, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise NotFoundError("Chapter")
    return chapter


@router.get("/projects/{project_id}/source", response_model=DocumentResponse)
def get_source_document(project_id: str, db: Session = Depends(get_db)):
    doc = db.query(SourceDocument).filter(SourceDocument.project_id == project_id).first()
    if not doc:
        raise NotFoundError("Source document")
    return doc
