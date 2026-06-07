from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from database import get_db
from models import ReviewIssue, QualityScore
from schemas import ReviewResponse, ReviewIssueResponse, QualityResponse, QualityDimension, GenerationResponse
from services.review_service import ReviewService
from exceptions import NotFoundError

router = APIRouter()


@router.post("/scripts/{script_id}/review", response_model=GenerationResponse)
def run_review(script_id: str, db: Session = Depends(get_db)):
    return ReviewService.run_review(db, script_id)


@router.get("/scripts/{script_id}/review", response_model=ReviewResponse)
def get_review(script_id: str, db: Session = Depends(get_db)):
    issues = db.query(ReviewIssue).filter(ReviewIssue.script_id == script_id).all()
    return ReviewResponse(
        reviewed_at=datetime.now(timezone.utc),
        model="mock-review-model",
        issues=[ReviewIssueResponse(
            id=i.id, type=i.type, severity=i.severity,
            scene_id=i.scene_id, beat_index=i.beat_index,
            message=i.message, suggestion=i.suggestion,
        ) for i in issues],
    )


@router.post("/scripts/{script_id}/quality", response_model=GenerationResponse)
def run_quality(script_id: str, db: Session = Depends(get_db)):
    return ReviewService.run_quality(db, script_id)


@router.get("/scripts/{script_id}/quality", response_model=QualityResponse)
def get_quality(script_id: str, db: Session = Depends(get_db)):
    quality = db.query(QualityScore).filter(QualityScore.script_id == script_id).first()
    if not quality:
        return QualityResponse(total_score=0, dimensions=[])
    return QualityResponse(
        total_score=quality.total_score,
        dimensions=[QualityDimension(**d) for d in (quality.dimensions or [])],
    )
