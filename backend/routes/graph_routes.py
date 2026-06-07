from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Character, Relationship, StoryEvent, Location
from schemas import (
    CharacterResponse, CharacterUpdate, RelationshipResponse,
    RelationshipUpdate, StoryGraphResponse, StoryEventResponse,
    LocationResponse, ExtractionResponse,
)
from services.graph_service import GraphService
from exceptions import NotFoundError

router = APIRouter()


@router.post("/projects/{project_id}/extract", response_model=ExtractionResponse)
def extract_graph(project_id: str, db: Session = Depends(get_db)):
    return GraphService.extract(db, project_id)


@router.get("/projects/{project_id}/characters", response_model=List[CharacterResponse])
def get_characters(project_id: str, db: Session = Depends(get_db)):
    characters = db.query(Character).filter(Character.project_id == project_id).all()
    result = []
    for c in characters:
        result.append(CharacterResponse(
            id=c.id, name=c.name, aliases=c.aliases or [],
            identity=c.identity, description=c.description,
            first_appearance={"chapter_id": c.first_chapter_id, "excerpt": c.first_excerpt} if c.first_chapter_id else None,
        ))
    return result


@router.get("/projects/{project_id}/relationships", response_model=List[RelationshipResponse])
def get_relationships(project_id: str, db: Session = Depends(get_db)):
    rels = db.query(Relationship).filter(Relationship.project_id == project_id).all()
    result = []
    for r in rels:
        result.append(RelationshipResponse(
            id=r.id, from_character_id=r.from_character_id, to_character_id=r.to_character_id,
            type=r.type, label=r.label, description=r.description,
            evidence={"chapter_id": r.evidence_chapter_id, "excerpt": r.evidence_excerpt} if r.evidence_chapter_id else None,
            confidence=r.confidence,
        ))
    return result


@router.get("/projects/{project_id}/story-graph", response_model=StoryGraphResponse)
def get_story_graph(project_id: str, db: Session = Depends(get_db)):
    events = db.query(StoryEvent).filter(StoryEvent.project_id == project_id).order_by(StoryEvent.timeline_order).all()
    locations = db.query(Location).filter(Location.project_id == project_id).all()

    event_responses = [StoryEventResponse(
        id=e.id, title=e.title, summary=e.summary, chapter_id=e.chapter_id,
        participants=e.participants or [], location_id=e.location_id,
        time_label=e.time_label, timeline_order=e.timeline_order,
        evidence={"excerpt": e.evidence_excerpt} if e.evidence_excerpt else None,
    ) for e in events]

    location_responses = [LocationResponse(id=l.id, name=l.name, description=l.description) for l in locations]
    timeline = [{"order": e.timeline_order, "event_id": e.id} for e in events]

    return StoryGraphResponse(events=event_responses, locations=location_responses, timeline=timeline)


@router.patch("/characters/{character_id}", response_model=CharacterResponse)
def update_character(character_id: str, update: CharacterUpdate, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise NotFoundError("Character")

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(character, field, value)

    db.commit()
    db.refresh(character)
    return CharacterResponse(
        id=character.id, name=character.name, aliases=character.aliases or [],
        identity=character.identity, description=character.description,
        first_appearance={"chapter_id": character.first_chapter_id, "excerpt": character.first_excerpt} if character.first_chapter_id else None,
    )


@router.patch("/relationships/{relationship_id}", response_model=RelationshipResponse)
def update_relationship(relationship_id: str, update: RelationshipUpdate, db: Session = Depends(get_db)):
    rel = db.query(Relationship).filter(Relationship.id == relationship_id).first()
    if not rel:
        raise NotFoundError("Relationship")

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(rel, field, value)

    db.commit()
    db.refresh(rel)
    return RelationshipResponse(
        id=rel.id, from_character_id=rel.from_character_id, to_character_id=rel.to_character_id,
        type=rel.type, label=rel.label, description=rel.description,
        evidence={"chapter_id": rel.evidence_chapter_id, "excerpt": rel.evidence_excerpt} if rel.evidence_chapter_id else None,
        confidence=rel.confidence,
    )
