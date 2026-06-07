from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone


def now_utc():
    return datetime.now(timezone.utc)

# String length constants
ID_LEN = 64
NAME_LEN = 255
STATUS_LEN = 32
TYPE_LEN = 64
PATH_LEN = 512


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    title = Column(String(NAME_LEN), index=True)
    description = Column(Text)
    creator = Column(String(NAME_LEN))
    status = Column(String(STATUS_LEN), default="draft")
    schema_version = Column(String(32), default="1.0")
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)

    source_document = relationship("SourceDocument", uselist=False, back_populates="project")
    chapters = relationship("Chapter", back_populates="project", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="project", cascade="all, delete-orphan")
    relationships = relationship("Relationship", back_populates="project", cascade="all, delete-orphan")
    story_events = relationship("StoryEvent", back_populates="project", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="project", cascade="all, delete-orphan")
    scripts = relationship("Script", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    export_files = relationship("ExportFile", back_populates="project", cascade="all, delete-orphan")


class SourceDocument(Base):
    __tablename__ = "source_documents"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    filename = Column(String(NAME_LEN))
    file_type = Column(String(16))
    language = Column(String(16))
    checksum = Column(String(64))
    file_path = Column(String(PATH_LEN))
    chapter_count = Column(Integer, default=0)
    total_characters = Column(Integer, default=0)
    parser_version = Column(String(64))

    project = relationship("Project", back_populates="source_document")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    index = Column(Integer)
    title = Column(String(NAME_LEN))
    summary = Column(Text)
    word_count = Column(Integer)
    content = Column(Text)

    project = relationship("Project", back_populates="chapters")


class Character(Base):
    __tablename__ = "characters"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(String(NAME_LEN), index=True)
    aliases = Column(JSON, default=list)
    identity = Column(String(NAME_LEN))
    description = Column(Text)
    first_chapter_id = Column(String(ID_LEN))
    first_excerpt = Column(Text)

    project = relationship("Project", back_populates="characters")


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    from_character_id = Column(String(ID_LEN))
    to_character_id = Column(String(ID_LEN))
    type = Column(String(TYPE_LEN))
    label = Column(String(NAME_LEN))
    description = Column(Text)
    evidence_chapter_id = Column(String(ID_LEN))
    evidence_excerpt = Column(Text)
    confidence = Column(Float)

    project = relationship("Project", back_populates="relationships")


class StoryEvent(Base):
    __tablename__ = "story_events"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    title = Column(String(NAME_LEN))
    summary = Column(Text)
    chapter_id = Column(String(ID_LEN))
    participants = Column(JSON, default=list)
    location_id = Column(String(ID_LEN))
    time_label = Column(String(NAME_LEN))
    timeline_order = Column(Integer)
    evidence_excerpt = Column(Text)

    project = relationship("Project", back_populates="story_events")


class Location(Base):
    __tablename__ = "locations"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    name = Column(String(NAME_LEN))
    description = Column(Text)

    project = relationship("Project", back_populates="locations")


class Script(Base):
    __tablename__ = "scripts"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    title = Column(String(NAME_LEN))
    style = Column(String(32))
    version = Column(String(32))
    logline = Column(Text)
    source_event_ids = Column(JSON, default=list)

    project = relationship("Project", back_populates="scripts")
    scenes = relationship("Scene", back_populates="script", cascade="all, delete-orphan")


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    script_id = Column(String(ID_LEN), ForeignKey("scripts.id", ondelete="CASCADE"))
    index = Column(Integer)
    title = Column(String(NAME_LEN))
    location = Column(String(NAME_LEN))
    time = Column(String(32))
    characters = Column(JSON, default=list)
    source_event_ids = Column(JSON, default=list)
    synopsis = Column(Text)

    script = relationship("Script", back_populates="scenes")
    beats = relationship("Beat", back_populates="scene", cascade="all, delete-orphan")


class Beat(Base):
    __tablename__ = "beats"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    scene_id = Column(String(ID_LEN), ForeignKey("scenes.id", ondelete="CASCADE"))
    index = Column(Integer)
    type = Column(String(32))
    content = Column(Text)
    character_id = Column(String(ID_LEN))
    character_name = Column(String(NAME_LEN))
    emotion = Column(String(64))

    scene = relationship("Scene", back_populates="beats")


class Shot(Base):
    __tablename__ = "shots"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    scene_id = Column(String(ID_LEN))
    index = Column(Integer)
    image_description = Column(Text)
    shot_size = Column(String(32))
    camera_movement = Column(String(32))
    lighting = Column(Text)
    duration_seconds = Column(Float)
    audio = Column(Text)

    project = relationship("Project")


class ReviewIssue(Base):
    __tablename__ = "review_issues"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    script_id = Column(String(ID_LEN))
    type = Column(String(TYPE_LEN))
    severity = Column(String(32))
    scene_id = Column(String(ID_LEN))
    beat_index = Column(Integer)
    message = Column(Text)
    suggestion = Column(Text)

    project = relationship("Project")


class QualityScore(Base):
    __tablename__ = "quality_scores"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    script_id = Column(String(ID_LEN))
    total_score = Column(Float)
    dimensions = Column(JSON, default=list)

    project = relationship("Project")


class ExportFile(Base):
    __tablename__ = "export_files"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    file_path = Column(String(PATH_LEN))
    exported_at = Column(DateTime, default=now_utc)
    exporter_version = Column(String(64))
    validated = Column(Boolean, default=False)
    validation_errors = Column(JSON, default=list)

    project = relationship("Project", back_populates="export_files")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(ID_LEN), primary_key=True, index=True)
    project_id = Column(String(ID_LEN), ForeignKey("projects.id", ondelete="CASCADE"))
    type = Column(String(TYPE_LEN))
    status = Column(String(STATUS_LEN), default="pending")
    progress = Column(Integer, default=0)
    message = Column(String(NAME_LEN))
    error = Column(Text)
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)

    project = relationship("Project", back_populates="tasks")
