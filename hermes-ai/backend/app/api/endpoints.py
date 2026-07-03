from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.pipeline import pipeline
from app.db.database import get_db, Base, engine
from app.db.repositories import JobRepository, CandidateRepository, RankingRepository
from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

router = APIRouter()

class JobRequest(BaseModel):
    description: str

class CandidateRequest(BaseModel):
    candidates: List[Dict[str, Any]]

class ReRankRequest(BaseModel):
    job_id: str
    weights: Dict[str, float]

@router.post("/job/analyze")
def analyze_job(req: JobRequest, db: Session = Depends(get_db)):
    job_profile = pipeline.analyze_job(req.description)
    repo = JobRepository(db)
    repo.save(job_profile.id, job_profile.role, job_profile.model_dump())
    return {"status": "success", "job_id": job_profile.id, "profile": job_profile.model_dump()}

@router.post("/candidate/analyze")
def analyze_candidates(req: CandidateRequest, db: Session = Depends(get_db)):
    repo = CandidateRepository(db)
    processed = []
    for c_raw in req.candidates:
        c_profile = pipeline.process_candidate(c_raw)
        repo.save(c_profile.id, c_profile.name, c_profile.model_dump())
        processed.append(c_profile.model_dump())
    return {"status": "success", "processed_count": len(processed), "candidates": processed}

@router.post("/rank/{job_id}")
def rank_candidates(job_id: str, db: Session = Depends(get_db)):
    job_repo = JobRepository(db)
    cand_repo = CandidateRepository(db)
    rank_repo = RankingRepository(db)

    job_data = job_repo.get(job_id)
    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")

    # We must convert dict back to Profile objects
    from app.domain.models import JobProfile, CandidateProfile
    job_profile = JobProfile(**job_data)

    candidates_data = cand_repo.get_all()
    rankings = []

    for c_data in candidates_data:
        c_profile = CandidateProfile(**c_data)
        ranking = pipeline.rank_candidate(job_profile, c_profile)
        rankings.append(ranking)

    # Sort and save
    rankings.sort(key=lambda r: r.overall_score, reverse=True)

    for r in rankings:
        rank_repo.save(job_profile.id, r.candidate_id, r.overall_score, r.model_dump())

    return {"status": "success", "rankings": [r.model_dump() for r in rankings]}

@router.post("/rankings/re-rank")
def rerank_candidates(req: ReRankRequest, db: Session = Depends(get_db)):
    rank_repo = RankingRepository(db)
    rankings_data = rank_repo.get_top_for_job(req.job_id)
    if not rankings_data:
        raise HTTPException(status_code=404, detail="No rankings found for this job")

    from app.domain.models import RankingDecision
    rankings = [RankingDecision(**r) for r in rankings_data]

    new_rankings = pipeline.counterfactual_engine.execute(rankings, req.weights)
    return {"status": "success", "rankings": [r.model_dump() for r in new_rankings]}

@router.get("/system/status")
def system_status():
    return {"status": "online", "engines": 12, "architecture": "Clean"}
