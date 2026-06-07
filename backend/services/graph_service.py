import re
from sqlalchemy.orm import Session
from models import Project, Chapter, Character, Relationship, StoryEvent, Location, Task
from utils import generate_id
from exceptions import NotFoundError, BadRequestError
from logger import logger


class GraphService:
    @staticmethod
    def extract_characters(chapters: list[Chapter]) -> list[dict]:
        characters = []
        names = set()
        patterns = [
            r"([\u4e00-\u9fa5]{2,4})\s*(?:是|作为|担任|叫|名叫)",
            r"(?:介绍|提到|出现)\s*([\u4e00-\u9fa5]{2,4})",
        ]
        for chapter in chapters:
            content = chapter.title + "\n" + (chapter.content or "")
            for pattern in patterns:
                for name in re.findall(pattern, content):
                    if name not in names and len(name) >= 2:
                        names.add(name)
                        characters.append({"name": name, "chapter_id": chapter.id, "excerpt": content[:50]})
        if not characters:
            characters = [{"name": "主角", "chapter_id": chapters[0].id if chapters else None, "excerpt": "主要人物"}]
        return characters

    @staticmethod
    def extract_relationships(characters: list[dict], chapters: list[Chapter]) -> list[dict]:
        relationships = []
        for i, c1 in enumerate(characters):
            for c2 in characters[i + 1:]:
                content = " ".join(ch.content or "" for ch in chapters)
                if c1["name"] in content and c2["name"] in content:
                    relationships.append({
                        "from_name": c1["name"], "to_name": c2["name"],
                        "type": "colleague", "label": "关联", "confidence": 0.7,
                    })
        return relationships

    @staticmethod
    def extract_events(chapters: list[Chapter]) -> tuple[list[dict], list[dict]]:
        events, locations, loc_names = [], [], set()
        for idx, ch in enumerate(chapters, 1):
            content = ch.content or ""
            events.append({
                "title": ch.title,
                "summary": content[:100] + "..." if len(content) > 100 else content,
                "chapter_id": ch.id, "participants": [],
                "location_name": "未知地点", "time_label": f"第{idx}章",
                "timeline_order": idx, "evidence": content[:50],
            })
            loc_name = f"场景{idx}"
            if loc_name not in loc_names:
                loc_names.add(loc_name)
                locations.append({"name": loc_name, "description": f"第{idx}章的场景"})
        return events, locations

    @staticmethod
    def extract(db: Session, project_id: str) -> dict:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project")

        chapters = db.query(Chapter).filter(Chapter.project_id == project_id).all()
        if not chapters:
            raise BadRequestError("No chapters found")

        task = Task(
            id=generate_id("task"), project_id=project_id,
            type="graph_extract", status="running", progress=30,
            message="正在抽取人物和事件...",
        )
        db.add(task)
        db.commit()

        # Clear existing data
        db.query(Character).filter(Character.project_id == project_id).delete()
        db.query(Relationship).filter(Relationship.project_id == project_id).delete()
        db.query(StoryEvent).filter(StoryEvent.project_id == project_id).delete()
        db.query(Location).filter(Location.project_id == project_id).delete()
        db.commit()

        # Extract and save characters
        chars_data = GraphService.extract_characters(chapters)
        char_name_to_id = {}
        for d in chars_data:
            char = Character(
                id=generate_id("char"), project_id=project_id,
                name=d["name"], aliases=[], identity="未指定",
                description=f"人物 {d['name']}",
                first_chapter_id=d["chapter_id"], first_excerpt=d["excerpt"],
            )
            db.add(char)
            char_name_to_id[d["name"]] = char.id

        # Extract and save relationships
        for rel in GraphService.extract_relationships(chars_data, chapters):
            from_id = char_name_to_id.get(rel["from_name"])
            to_id = char_name_to_id.get(rel["to_name"])
            if from_id and to_id:
                db.add(Relationship(
                    id=generate_id("rel"), project_id=project_id,
                    from_character_id=from_id, to_character_id=to_id,
                    type=rel["type"], label=rel["label"],
                    description=f"{rel['from_name']} 与 {rel['to_name']} 的关系",
                    confidence=rel["confidence"],
                ))

        # Extract and save events & locations
        events_data, locs_data = GraphService.extract_events(chapters)
        loc_name_to_id = {}
        for loc in locs_data:
            location = Location(id=generate_id("loc"), project_id=project_id, name=loc["name"], description=loc["description"])
            db.add(location)
            loc_name_to_id[loc["name"]] = location.id

        char_ids = list(char_name_to_id.values())
        for ev in events_data:
            db.add(StoryEvent(
                id=generate_id("event"), project_id=project_id,
                title=ev["title"], summary=ev["summary"],
                chapter_id=ev["chapter_id"],
                participants=[char_ids[0]] if char_ids else [],
                location_id=loc_name_to_id.get(ev["location_name"]),
                time_label=ev["time_label"], timeline_order=ev["timeline_order"],
                evidence_excerpt=ev["evidence"],
            ))

        task.status = "succeeded"
        task.progress = 100
        task.message = "图谱抽取完成"
        project.status = "reviewing"
        db.commit()
        logger.info(f"Graph extracted for project {project_id}")
        return {"task_id": task.id, "message": "图谱抽取完成"}
