from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json

from database import get_db
from models import Script, Scene, Beat
from schemas import ScriptCreate, ScriptResponse, SceneResponse, SceneCreate, SceneUpdate, BeatResponse, GenerationResponse
from services.script_service import ScriptService
from exceptions import NotFoundError

router = APIRouter()


@router.post("/projects/{project_id}/scripts", response_model=GenerationResponse)
def create_script(project_id: str, data: ScriptCreate, db: Session = Depends(get_db)):
    return ScriptService.create(db, project_id, data.style, data.version)


@router.get("/scripts/{script_id}", response_model=ScriptResponse)
def get_script(script_id: str, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise NotFoundError("Script")

    scenes = db.query(Scene).filter(Scene.script_id == script_id).order_by(Scene.index).all()
    scene_responses = []
    for scene in scenes:
        beats = db.query(Beat).filter(Beat.scene_id == scene.id).order_by(Beat.index).all()
        scene_responses.append(SceneResponse(
            id=scene.id, index=scene.index, title=scene.title,
            location=scene.location, time=scene.time,
            characters=scene.characters or [], source_event_ids=scene.source_event_ids or [],
            synopsis=scene.synopsis,
            beats=[BeatResponse(id=b.id, type=b.type, content=b.content, character_id=b.character_id, character_name=b.character_name, emotion=b.emotion) for b in beats],
        ))

    return ScriptResponse(
        id=script.id, title=script.title, style=script.style,
        version=script.version, logline=script.logline,
        source_event_ids=script.source_event_ids or [],
        scenes=scene_responses,
    )


@router.patch("/scripts/{script_id}", response_model=ScriptResponse)
def update_script(script_id: str, update: dict, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise NotFoundError("Script")
    for key in ("title", "style", "logline"):
        if key in update:
            setattr(script, key, update[key])
    db.commit()
    return get_script(script_id, db)


@router.post("/scripts/{script_id}/scenes", response_model=SceneResponse)
def add_scene(script_id: str, data: SceneCreate, db: Session = Depends(get_db)):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise NotFoundError("Script")

    scene_count = db.query(Scene).filter(Scene.script_id == script_id).count()
    scene = Scene(
        id=generate_id("scene"), script_id=script_id, index=scene_count + 1,
        title=data.title, location=data.location, time=data.time,
        characters=data.characters, source_event_ids=data.source_event_ids or [],
        synopsis=data.synopsis,
    )
    db.add(scene)
    db.commit()
    db.refresh(scene)

    if data.beats:
        for idx, b in enumerate(data.beats, 1):
            db.add(Beat(
                id=generate_id("beat"), scene_id=scene.id, index=idx,
                type=b.type, content=b.content, character_id=b.character_id,
                character_name=b.character_name, emotion=b.emotion,
            ))
        db.commit()

    return get_scene(scene.id, db)


@router.patch("/scenes/{scene_id}", response_model=SceneResponse)
def update_scene(scene_id: str, data: SceneUpdate, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise NotFoundError("Scene")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(scene, field, value)
    db.commit()
    db.refresh(scene)

    beats = db.query(Beat).filter(Beat.scene_id == scene.id).order_by(Beat.index).all()
    return SceneResponse(
        id=scene.id, index=scene.index, title=scene.title,
        location=scene.location, time=scene.time,
        characters=scene.characters or [], source_event_ids=scene.source_event_ids or [],
        synopsis=scene.synopsis,
        beats=[BeatResponse(id=b.id, type=b.type, content=b.content, character_id=b.character_id, character_name=b.character_name, emotion=b.emotion) for b in beats],
    )


@router.delete("/scenes/{scene_id}")
def delete_scene(scene_id: str, db: Session = Depends(get_db)):
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise NotFoundError("Scene")
    script_id = scene.script_id
    db.query(Beat).filter(Beat.scene_id == scene_id).delete()
    db.delete(scene)
    db.commit()
    for idx, s in enumerate(db.query(Scene).filter(Scene.script_id == script_id).order_by(Scene.index).all(), 1):
        s.index = idx
    db.commit()
    return {"message": "Scene deleted"}


def generate_id(prefix: str) -> str:
    from uuid import uuid4
    return f"{prefix}_{uuid4().hex[:8]}"
