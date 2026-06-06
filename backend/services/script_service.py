from sqlalchemy.orm import Session
from models import Project, Character, StoryEvent, Script, Scene, Beat, Task
from utils import generate_id
from exceptions import NotFoundError
from logger import logger


STYLE_CONFIG = {
    "film": {"scene_count": 5, "beat_count": 4},
    "tv_series": {"scene_count": 8, "beat_count": 5},
    "short_drama": {"scene_count": 3, "beat_count": 3},
    "animation": {"scene_count": 6, "beat_count": 4},
}


class ScriptService:
    @staticmethod
    def _generate_script_data(project_id: str, style: str, db: Session) -> dict:
        characters = db.query(Character).filter(Character.project_id == project_id).all()
        events = db.query(StoryEvent).filter(StoryEvent.project_id == project_id).order_by(StoryEvent.timeline_order).all()

        char_ids = [c.id for c in characters]
        char_names = {c.id: c.name for c in characters}
        config = STYLE_CONFIG.get(style, STYLE_CONFIG["film"])

        scenes = []
        for i in range(min(config["scene_count"], len(events))):
            event = events[i] if i < len(events) else None
            beats = []
            for j in range(config["beat_count"]):
                if j == 0:
                    beats.append({"type": "action", "content": f"场景{i+1}开场动作描述..."})
                elif j == 1 and char_ids:
                    beats.append({"type": "dialogue", "character_id": char_ids[0], "character_name": char_names[char_ids[0]], "content": "对话内容..."})
                elif j % 2 == 0:
                    beats.append({"type": "action", "content": f"动作描述 {j}..."})
                else:
                    beats.append({"type": "dialogue", "character_id": char_ids[0] if char_ids else None, "character_name": char_names.get(char_ids[0]) if char_ids else None, "content": f"对话 {j}..."})

            scenes.append({
                "title": f"场次{i+1}: {event.title if event else f'场景{i+1}'}",
                "location": "室内/室外", "time": "日/夜",
                "characters": char_ids[:3],
                "source_event_ids": [event.id] if event else [],
                "synopsis": event.summary if event else f"场次{i+1}概要",
                "beats": beats,
            })

        return {"title": f"剧本 - {style}", "style": style, "logline": "故事梗概...", "scenes": scenes}

    @staticmethod
    def create(db: Session, project_id: str, style: str, version: str = None) -> dict:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project")

        task = Task(
            id=generate_id("task"), project_id=project_id,
            type="script_generation", status="running", progress=40,
            message="正在生成剧本...",
        )
        db.add(task)
        db.commit()

        db.query(Script).filter(Script.project_id == project_id).delete()
        db.commit()

        data = ScriptService._generate_script_data(project_id, style, db)
        script = Script(
            id=generate_id("script"), project_id=project_id,
            title=data["title"], style=style,
            version=version or "v1", logline=data["logline"],
            source_event_ids=[],
        )
        db.add(script)
        db.commit()
        db.refresh(script)

        for idx, s in enumerate(data["scenes"], 1):
            scene = Scene(
                id=generate_id("scene"), script_id=script.id, index=idx,
                title=s["title"], location=s["location"], time=s["time"],
                characters=s["characters"], source_event_ids=s["source_event_ids"],
                synopsis=s["synopsis"],
            )
            db.add(scene)
            db.commit()
            db.refresh(scene)
            for b_idx, b in enumerate(s["beats"], 1):
                db.add(Beat(
                    id=generate_id("beat"), scene_id=scene.id, index=b_idx,
                    type=b["type"], content=b["content"],
                    character_id=b.get("character_id"), character_name=b.get("character_name"),
                    emotion=b.get("emotion"),
                ))

        task.status = "succeeded"
        task.progress = 100
        task.message = "剧本生成完成"
        db.commit()
        logger.info(f"Script generated for project {project_id}")
        return {"task_id": task.id, "message": "剧本生成完成"}
