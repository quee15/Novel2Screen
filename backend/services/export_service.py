import os
import yaml
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import (
    Project, SourceDocument, Chapter, Character, Relationship,
    StoryEvent, Location, Script, Scene, Beat, Shot,
    ReviewIssue, QualityScore, ExportFile,
)
from utils import generate_id
from exceptions import NotFoundError
from config import get_settings
from logger import logger

settings = get_settings()


class ExportService:
    @staticmethod
    def _validate(data: dict) -> list[str]:
        errors = []
        if "schema_version" not in data:
            errors.append("缺少 schema_version")
        if "project" not in data or "id" not in data.get("project", {}):
            errors.append("缺少 project 或 project.id")
        if "source" not in data or "document" not in data.get("source", {}):
            errors.append("缺少 source 或 source.document")
        if "script" not in data or not data.get("script", {}).get("scenes"):
            errors.append("缺少 script 或 script.scenes 为空")
        return errors

    @staticmethod
    def _build_model(project_id: str, db: Session) -> dict:
        project = db.query(Project).filter(Project.id == project_id).first()
        src = db.query(SourceDocument).filter(SourceDocument.project_id == project_id).first()
        chapters = db.query(Chapter).filter(Chapter.project_id == project_id).order_by(Chapter.index).all()
        characters = db.query(Character).filter(Character.project_id == project_id).all()
        relationships = db.query(Relationship).filter(Relationship.project_id == project_id).all()
        events = db.query(StoryEvent).filter(StoryEvent.project_id == project_id).order_by(StoryEvent.timeline_order).all()
        locations = db.query(Location).filter(Location.project_id == project_id).all()
        scripts = db.query(Script).filter(Script.project_id == project_id).all()
        script = scripts[0] if scripts else None

        scenes = []
        scene_beats = []
        if script:
            scenes = db.query(Scene).filter(Scene.script_id == script.id).order_by(Scene.index).all()
            for scene in scenes:
                scene_beats.extend(db.query(Beat).filter(Beat.scene_id == scene.id).order_by(Beat.index).all())

        shots = db.query(Shot).filter(Shot.project_id == project_id).order_by(Shot.scene_id, Shot.index).all()
        review_issues = db.query(ReviewIssue).filter(ReviewIssue.project_id == project_id).all()
        quality = db.query(QualityScore).filter(QualityScore.project_id == project_id).first()

        def _dt(dt):
            return dt.isoformat() if dt else None

        return {
            "schema_version": "1.0",
            "project": {"id": project.id, "title": project.title, "description": project.description, "creator": project.creator, "created_at": _dt(project.created_at), "updated_at": _dt(project.updated_at), "status": project.status},
            "source": {
                "document": {"id": src.id if src else "", "filename": src.filename if src else "", "file_type": src.file_type if src else "", "language": src.language if src else "", "checksum": src.checksum if src else ""},
                "parse_result": {"chapter_count": src.chapter_count if src else 0, "total_characters": src.total_characters if src else 0, "parser_version": src.parser_version if src else ""},
                "chapters": [{"id": ch.id, "index": ch.index, "title": ch.title, "summary": ch.summary, "word_count": ch.word_count} for ch in chapters],
            },
            "characters": [{"id": c.id, "name": c.name, "aliases": c.aliases or [], "identity": c.identity, "description": c.description, "first_appearance": {"chapter_id": c.first_chapter_id, "excerpt": c.first_excerpt} if c.first_chapter_id else None} for c in characters],
            "relationships": [{"id": r.id, "from_character_id": r.from_character_id, "to_character_id": r.to_character_id, "type": r.type, "label": r.label, "description": r.description, "evidence": {"chapter_id": r.evidence_chapter_id, "excerpt": r.evidence_excerpt} if r.evidence_chapter_id else None, "confidence": r.confidence} for r in relationships],
            "story_graph": {
                "events": [{"id": e.id, "title": e.title, "summary": e.summary, "chapter_id": e.chapter_id, "participants": e.participants or [], "location_id": e.location_id, "time_label": e.time_label, "timeline_order": e.timeline_order, "evidence": {"excerpt": e.evidence_excerpt} if e.evidence_excerpt else None} for e in events],
                "locations": [{"id": l.id, "name": l.name, "description": l.description} for l in locations],
                "timeline": [{"order": e.timeline_order, "event_id": e.id} for e in events],
            },
            "script": {
                "id": script.id if script else "", "title": script.title if script else "", "style": script.style if script else "", "version": script.version if script else "", "logline": script.logline if script else "",
                "source_event_ids": script.source_event_ids if script else [],
                "scenes": [{"id": s.id, "index": s.index, "title": s.title, "location": s.location, "time": s.time, "characters": s.characters or [], "source_event_ids": s.source_event_ids or [], "synopsis": s.synopsis, "beats": [{"id": b.id, "type": b.type, "content": b.content, "character_id": b.character_id, "character_name": b.character_name, "emotion": b.emotion} for b in scene_beats if b.scene_id == s.id]} for s in scenes],
            },
            "storyboard": {"shots": [{"id": sh.id, "scene_id": sh.scene_id, "index": sh.index, "image_description": sh.image_description, "shot_size": sh.shot_size, "camera_movement": sh.camera_movement, "lighting": sh.lighting, "duration_seconds": sh.duration_seconds, "audio": sh.audio} for sh in shots]},
            "review": {"reviewed_at": datetime.now(timezone.utc).isoformat(), "model": "mock-model", "issues": [{"id": i.id, "type": i.type, "severity": i.severity, "scene_id": i.scene_id, "beat_index": i.beat_index, "message": i.message, "suggestion": i.suggestion} for i in review_issues]},
            "quality": {"total_score": quality.total_score if quality else 0, "dimensions": quality.dimensions if quality else []},
            "export": {"exported_at": datetime.now(timezone.utc).isoformat(), "exporter_version": "exporter-1.0", "validated": True, "validation_errors": []},
            "extensions": {},
        }

    @staticmethod
    def export_yaml(db: Session, project_id: str) -> dict:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project")

        model = ExportService._build_model(project_id, db)
        errors = ExportService._validate(model)
        validated = len(errors) == 0

        export_dir = settings.EXPORT_DIR
        os.makedirs(export_dir, exist_ok=True)

        export_id = generate_id("export")
        file_path = os.path.join(export_dir, f"{project_id}.yaml")

        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(model, f, allow_unicode=True, sort_keys=False)

        db.add(ExportFile(
            id=export_id, project_id=project_id, file_path=file_path,
            exporter_version="exporter-1.0", validated=validated, validation_errors=errors,
        ))
        db.commit()
        logger.info(f"YAML exported for project {project_id}")
        return {
            "id": export_id, "project_id": project_id,
            "exported_at": datetime.now(timezone.utc),
            "exporter_version": "exporter-1.0",
            "validated": validated, "validation_errors": errors,
        }
