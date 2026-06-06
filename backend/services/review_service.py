from sqlalchemy.orm import Session
from models import Script, Scene, ReviewIssue, QualityScore, Task
from utils import generate_id
from exceptions import NotFoundError
from logger import logger


class ReviewService:
    @staticmethod
    def _generate_issues(script_id: str, db: Session) -> list[dict]:
        scenes = db.query(Scene).filter(Scene.script_id == script_id).all()
        templates = [
            ("character_consistency", "low", "人物一致性检查"),
            ("timeline", "medium", "时间线检查"),
            ("scene_integrity", "low", "场景完整性"),
            ("dialogue_distribution", "medium", "对白分布"),
        ]
        issues = []
        for scene in scenes:
            for idx, (type_, severity, msg) in enumerate(templates):
                if idx % 2 == 0:
                    issues.append({
                        "type": type_, "severity": severity, "scene_id": scene.id,
                        "beat_index": idx + 1,
                        "message": f"{msg}: 场景{scene.index}可能存在{msg.lower()}问题",
                        "suggestion": f"建议检查并优化{msg.lower()}相关内容",
                    })
        return issues

    @staticmethod
    def _calculate_quality(issue_count: int) -> dict:
        dimensions = [
            {"name": "完整性", "key": "completeness", "base_score": 85},
            {"name": "一致性", "key": "consistency", "base_score": 80},
            {"name": "场景连续性", "key": "scene_continuity", "base_score": 75},
            {"name": "对白分布", "key": "dialogue_distribution", "base_score": 82},
        ]
        penalty = min(issue_count * 2, 20)
        for dim in dimensions:
            dim["score"] = max(0, dim["base_score"] - penalty)
            dim["comment"] = f"{dim['name']}评分: {dim['score']}"
        total = round(sum(d["score"] for d in dimensions) / len(dimensions), 1)
        return {"total_score": total, "dimensions": dimensions}

    @staticmethod
    def run_review(db: Session, script_id: str) -> dict:
        script = db.query(Script).filter(Script.id == script_id).first()
        if not script:
            raise NotFoundError("Script")

        task = Task(
            id=generate_id("task"), project_id=script.project_id,
            type="script_review", status="running", progress=35,
            message="正在执行 AI 审校...",
        )
        db.add(task)
        db.commit()

        db.query(ReviewIssue).filter(ReviewIssue.script_id == script_id).delete()
        db.commit()

        for d in ReviewService._generate_issues(script_id, db):
            db.add(ReviewIssue(
                id=generate_id("issue"), project_id=script.project_id,
                script_id=script_id, type=d["type"], severity=d["severity"],
                scene_id=d["scene_id"], beat_index=d["beat_index"],
                message=d["message"], suggestion=d["suggestion"],
            ))

        task.status = "succeeded"
        task.progress = 100
        issue_count = db.query(ReviewIssue).filter(ReviewIssue.script_id == script_id).count()
        task.message = f"审校完成，发现 {issue_count} 个问题"
        db.commit()
        logger.info(f"Review completed for script {script_id}")
        return {"task_id": task.id, "message": "审校完成"}

    @staticmethod
    def run_quality(db: Session, script_id: str) -> dict:
        script = db.query(Script).filter(Script.id == script_id).first()
        if not script:
            raise NotFoundError("Script")

        issue_count = db.query(ReviewIssue).filter(ReviewIssue.script_id == script_id).count()
        task = Task(
            id=generate_id("task"), project_id=script.project_id,
            type="quality_scoring", status="running", progress=35,
            message="正在计算质量评分...",
        )
        db.add(task)
        db.commit()

        db.query(QualityScore).filter(QualityScore.script_id == script_id).delete()
        db.commit()

        quality_data = ReviewService._calculate_quality(issue_count)
        db.add(QualityScore(
            id=generate_id("quality"), project_id=script.project_id,
            script_id=script_id, total_score=quality_data["total_score"],
            dimensions=quality_data["dimensions"],
        ))

        task.status = "succeeded"
        task.progress = 100
        task.message = f"评分完成，总分 {quality_data['total_score']}"
        db.commit()
        logger.info(f"Quality scored for script {script_id}: {quality_data['total_score']}")
        return {"task_id": task.id, "message": "质量评分完成"}
