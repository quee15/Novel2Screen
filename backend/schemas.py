from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    draft = "draft"
    processing = "processing"
    reviewing = "reviewing"
    completed = "completed"
    archived = "archived"

class FileType(str, Enum):
    txt = "txt"
    docx = "docx"

class ScriptStyle(str, Enum):
    film = "film"
    tv_series = "tv_series"
    short_drama = "short_drama"
    animation = "animation"

class BeatType(str, Enum):
    action = "action"
    dialogue = "dialogue"
    transition = "transition"
    note = "note"

class ShotSize(str, Enum):
    extreme_wide = "extreme_wide"
    wide = "wide"
    medium = "medium"
    close_up = "close_up"
    extreme_close_up = "extreme_close_up"

class CameraMovement(str, Enum):
    static = "static"
    pan = "pan"
    tilt = "tilt"
    dolly = "dolly"
    tracking = "tracking"
    handheld = "handheld"
    slow_push_in = "slow_push_in"

class ReviewIssueType(str, Enum):
    character_consistency = "character_consistency"
    timeline = "timeline"
    scene_integrity = "scene_integrity"
    dialogue_distribution = "dialogue_distribution"
    continuity = "continuity"
    other = "other"

class IssueSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    canceled = "canceled"

class RelationshipType(str, Enum):
    family = "family"
    enemy = "enemy"
    ally = "ally"
    lover = "lover"
    mentor = "mentor"
    student = "student"
    colleague = "colleague"
    unknown = "unknown"

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    creator: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None

class ProjectResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    creator: Optional[str]
    status: ProjectStatus
    schema_version: str
    created_at: datetime
    updated_at: datetime

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: FileType
    language: Optional[str]
    checksum: Optional[str]
    chapter_count: int
    total_characters: int
    parser_version: Optional[str]

class ChapterResponse(BaseModel):
    id: str
    index: int
    title: str
    summary: Optional[str]
    word_count: Optional[int]

class ChapterDetailResponse(ChapterResponse):
    content: Optional[str]

class CharacterCreate(BaseModel):
    name: str
    aliases: Optional[List[str]] = []
    identity: Optional[str] = None
    description: Optional[str] = None
    first_chapter_id: Optional[str] = None
    first_excerpt: Optional[str] = None

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    aliases: Optional[List[str]] = None
    identity: Optional[str] = None
    description: Optional[str] = None

class CharacterResponse(BaseModel):
    id: str
    name: str
    aliases: List[str]
    identity: Optional[str]
    description: Optional[str]
    first_appearance: Optional[Dict[str, str]]

class RelationshipCreate(BaseModel):
    from_character_id: str
    to_character_id: str
    type: RelationshipType
    label: str
    description: Optional[str] = None
    evidence_chapter_id: Optional[str] = None
    evidence_excerpt: Optional[str] = None
    confidence: Optional[float] = None

class RelationshipUpdate(BaseModel):
    type: Optional[RelationshipType] = None
    label: Optional[str] = None
    description: Optional[str] = None

class RelationshipResponse(BaseModel):
    id: str
    from_character_id: str
    to_character_id: str
    type: RelationshipType
    label: str
    description: Optional[str]
    evidence: Optional[Dict[str, str]]
    confidence: Optional[float]

class StoryEventResponse(BaseModel):
    id: str
    title: str
    summary: str
    chapter_id: str
    participants: List[str]
    location_id: Optional[str]
    time_label: Optional[str]
    timeline_order: int
    evidence: Optional[Dict[str, str]]

class LocationResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]

class StoryGraphResponse(BaseModel):
    events: List[StoryEventResponse]
    locations: List[LocationResponse]
    timeline: List[Dict[str, Any]]

class BeatResponse(BaseModel):
    id: str
    type: BeatType
    content: str
    character_id: Optional[str]
    character_name: Optional[str]
    emotion: Optional[str]

class BeatCreate(BaseModel):
    type: BeatType
    content: str
    character_id: Optional[str] = None
    character_name: Optional[str] = None
    emotion: Optional[str] = None

class SceneResponse(BaseModel):
    id: str
    index: int
    title: str
    location: str
    time: str
    characters: List[str]
    source_event_ids: Optional[List[str]]
    synopsis: Optional[str]
    beats: List[BeatResponse]

class SceneCreate(BaseModel):
    title: str
    location: str
    time: str
    characters: List[str]
    source_event_ids: Optional[List[str]] = None
    synopsis: Optional[str] = None
    beats: Optional[List[BeatCreate]] = None

class SceneUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    time: Optional[str] = None
    synopsis: Optional[str] = None

class ScriptCreate(BaseModel):
    style: ScriptStyle
    version: Optional[str] = None

class ScriptResponse(BaseModel):
    id: str
    title: str
    style: ScriptStyle
    version: str
    logline: Optional[str]
    source_event_ids: Optional[List[str]]
    scenes: List[SceneResponse]

class ReviewIssueResponse(BaseModel):
    id: str
    type: ReviewIssueType
    severity: IssueSeverity
    scene_id: Optional[str]
    beat_index: Optional[int]
    message: str
    suggestion: str

class ReviewResponse(BaseModel):
    reviewed_at: datetime
    model: Optional[str]
    issues: List[ReviewIssueResponse]

class QualityDimension(BaseModel):
    name: str
    key: str
    score: float
    comment: str

class QualityResponse(BaseModel):
    total_score: float
    dimensions: List[QualityDimension]

class ShotResponse(BaseModel):
    id: str
    scene_id: str
    index: int
    image_description: str
    shot_size: ShotSize
    camera_movement: CameraMovement
    lighting: Optional[str]
    duration_seconds: Optional[float]
    audio: Optional[str]

class StoryboardResponse(BaseModel):
    shots: List[ShotResponse]

class ExportResponse(BaseModel):
    id: str
    project_id: str
    exported_at: datetime
    exporter_version: str
    validated: bool
    validation_errors: List[str]

class TaskResponse(BaseModel):
    id: str
    project_id: str
    type: str
    status: TaskStatus
    progress: int
    message: Optional[str]
    error: Optional[str]
    created_at: datetime
    updated_at: datetime

class ExtractionResponse(BaseModel):
    task_id: str
    message: str

class GenerationResponse(BaseModel):
    task_id: str
    message: str