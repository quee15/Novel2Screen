from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Shot
from schemas import StoryboardResponse, ShotResponse, GenerationResponse
from services.storyboard_service import StoryboardService
from exceptions import NotFoundError

router = APIRouter()


@router.post("/scripts/{script_id}/storyboard", response_model=GenerationResponse)
def generate_storyboard(script_id: str, db: Session = Depends(get_db)):
    return StoryboardService.generate(db, script_id)


@router.get("/scripts/{script_id}/storyboard", response_model=StoryboardResponse)
def get_storyboard(script_id: str, db: Session = Depends(get_db)):
    from models import Script
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise NotFoundError("Script")

    shots = db.query(Shot).filter(Shot.project_id == script.project_id).order_by(Shot.scene_id, Shot.index).all()
    return StoryboardResponse(shots=[ShotResponse(
        id=s.id, scene_id=s.scene_id, index=s.index,
        image_description=s.image_description, shot_size=s.shot_size,
        camera_movement=s.camera_movement, lighting=s.lighting,
        duration_seconds=s.duration_seconds, audio=s.audio,
    ) for s in shots])


@router.patch("/shots/{shot_id}", response_model=ShotResponse)
def update_shot(shot_id: str, update: dict, db: Session = Depends(get_db)):
    shot = db.query(Shot).filter(Shot.id == shot_id).first()
    if not shot:
        raise NotFoundError("Shot")
    for key in ("image_description", "shot_size", "camera_movement", "lighting", "duration_seconds", "audio"):
        if key in update:
            setattr(shot, key, update[key])
    db.commit()
    db.refresh(shot)
    return ShotResponse(
        id=shot.id, scene_id=shot.scene_id, index=shot.index,
        image_description=shot.image_description, shot_size=shot.shot_size,
        camera_movement=shot.camera_movement, lighting=shot.lighting,
        duration_seconds=shot.duration_seconds, audio=shot.audio,
    )


@router.post("/scenes/{scene_id}/storyboard/regenerate", response_model=GenerationResponse)
def regenerate_scene_storyboard(scene_id: str, db: Session = Depends(get_db)):
    return StoryboardService.regenerate_scene(db, scene_id)
