from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
import os

from database import get_db
from models import ExportFile
from schemas import ExportResponse
from services.export_service import ExportService
from exceptions import NotFoundError

router = APIRouter()


@router.post("/projects/{project_id}/exports/yaml", response_model=ExportResponse)
def export_yaml(project_id: str, db: Session = Depends(get_db)):
    result = ExportService.export_yaml(db, project_id)
    return ExportResponse(**result)


@router.get("/exports/{export_id}", response_model=ExportResponse)
def get_export(export_id: str, db: Session = Depends(get_db)):
    export_file = db.query(ExportFile).filter(ExportFile.id == export_id).first()
    if not export_file:
        raise NotFoundError("Export")
    return ExportResponse(
        id=export_file.id, project_id=export_file.project_id,
        exported_at=export_file.exported_at, exporter_version=export_file.exporter_version,
        validated=export_file.validated, validation_errors=export_file.validation_errors or [],
    )


@router.get("/exports/{export_id}/download")
def download_export(export_id: str, db: Session = Depends(get_db)):
    export_file = db.query(ExportFile).filter(ExportFile.id == export_id).first()
    if not export_file:
        raise NotFoundError("Export")
    if not os.path.exists(export_file.file_path):
        raise NotFoundError("Export file")
    return FileResponse(export_file.file_path, media_type="text/yaml", filename=os.path.basename(export_file.file_path))
