from sqlalchemy.orm import Session
from models import Script, Scene, Shot, Task
from utils import generate_id
from exceptions import NotFoundError
from logger import logger

SHOT_SIZES = ["extreme_wide", "wide", "medium", "close_up", "extreme_close_up"]
CAMERA_MOVEMENTS = ["static", "pan", "tilt", "dolly", "tracking", "handheld", "slow_push_in"]


class StoryboardService:
    @staticmethod
    def _generate_shots(scene_id: str, scene_index: int, scene_title: str) -> list[dict]:
        shots = []
        for i in range(3):
            shots.append({
                "scene_id": scene_id, "index": i + 1,
                "image_description": f"{scene_title} - 镜头{i+1}画面描述",
                "shot_size": SHOT_SIZES[i % len(SHOT_SIZES)],
                "camera_movement": CAMERA_MOVEMENTS[i % len(CAMERA_MOVEMENTS)],
                "lighting": "建议使用自然光线或人工布光",
                "duration_seconds": 5 + i * 2,
                "audio": "环境音效",
            })
        return shots

    @staticmethod
    def generate(db: Session, script_id: str) -> dict:
        script = db.query(Script).filter(Script.id == script_id).first()
        if not script:
            raise NotFoundError("Script")

        task = Task(
            id=generate_id("task"), project_id=script.project_id,
            type="storyboard_generation", status="running", progress=35,
            message="正在生成分镜...",
        )
        db.add(task)
        db.commit()

        db.query(Shot).filter(Shot.project_id == script.project_id).delete()
        db.commit()

        scenes = db.query(Scene).filter(Scene.script_id == script_id).order_by(Scene.index).all()
        for scene in scenes:
            for d in StoryboardService._generate_shots(scene.id, scene.index, scene.title):
                db.add(Shot(
                    id=generate_id("shot"), project_id=script.project_id,
                    scene_id=d["scene_id"], index=d["index"],
                    image_description=d["image_description"],
                    shot_size=d["shot_size"], camera_movement=d["camera_movement"],
                    lighting=d["lighting"], duration_seconds=d["duration_seconds"],
                    audio=d["audio"],
                ))

        task.status = "succeeded"
        task.progress = 100
        task.message = "分镜生成完成"
        db.commit()
        logger.info(f"Storyboard generated for script {script_id}")
        return {"task_id": task.id, "message": "分镜生成完成"}

    @staticmethod
    def regenerate_scene(db: Session, scene_id: str) -> dict:
        scene = db.query(Scene).filter(Scene.id == scene_id).first()
        if not scene:
            raise NotFoundError("Scene")

        db.query(Shot).filter(Shot.scene_id == scene_id).delete()
        for d in StoryboardService._generate_shots(scene.id, scene.index, scene.title):
            db.add(Shot(
                id=generate_id("shot"), project_id=scene.script.project_id,
                scene_id=d["scene_id"], index=d["index"],
                image_description=d["image_description"],
                shot_size=d["shot_size"], camera_movement=d["camera_movement"],
                lighting=d["lighting"], duration_seconds=d["duration_seconds"],
                audio=d["audio"],
            ))
        db.commit()
        logger.info(f"Storyboard regenerated for scene {scene_id}")
        return {"task_id": generate_id("task"), "message": "单场分镜已重新生成"}
