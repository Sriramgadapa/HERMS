from sqlalchemy.orm import Session
from .models import DBJob, DBCandidate, DBRanking
import json

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, job_id: str, role: str, job_profile_data: dict):
        db_job = DBJob(id=job_id, role=role, data=job_profile_data)
        self.db.merge(db_job)
        self.db.commit()
        return db_job

    def get(self, job_id: str):
        job = self.db.query(DBJob).filter(DBJob.id == job_id).first()
        return job.data if job else None

class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, candidate_id: str, name: str, profile_data: dict):
        db_candidate = DBCandidate(id=candidate_id, name=name, data=profile_data)
        self.db.merge(db_candidate)
        self.db.commit()
        return db_candidate

    def get_all(self):
        candidates = self.db.query(DBCandidate).all()
        return [c.data for c in candidates]

class RankingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, job_id: str, candidate_id: str, score: float, data: dict):
        db_ranking = DBRanking(job_id=job_id, candidate_id=candidate_id, overall_score=score, data=data)
        self.db.add(db_ranking)
        self.db.commit()
        return db_ranking

    def get_top_for_job(self, job_id: str, limit: int = 100):
        rankings = self.db.query(DBRanking).filter(DBRanking.job_id == job_id).order_by(DBRanking.overall_score.desc()).limit(limit).all()
        return [r.data for r in rankings]
