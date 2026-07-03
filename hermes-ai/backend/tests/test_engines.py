import pytest
from app.ai.engines.job_intelligence import JobIntelligenceEngine
from app.ai.engines.candidate_intelligence import CandidateIntelligenceEngine
from app.ai.engines.hidden_skill import HiddenSkillInferenceEngine
from app.ai.engines.technical_fit import TechnicalFitEngine
from app.ai.engines.counterfactual import CounterfactualEngine
from app.domain.models import JobProfile, CandidateProfile, RankingDecision

def test_job_engine():
    engine = JobIntelligenceEngine()
    jd = "Looking for a Python backend engineer with FastAPI and Docker experience."
    profile = engine.execute(jd)
    assert "Python" in profile.required_skills
    assert "FastAPI" in profile.required_skills
    assert "Docker" in profile.preferred_skills

def test_candidate_and_hidden_skill():
    c_engine = CandidateIntelligenceEngine()
    h_engine = HiddenSkillInferenceEngine()

    raw = {
        "id": "123",
        "name": "Alice",
        "skills": ["Kafka", "Redis", "Docker"]
    }

    profile = c_engine.execute(raw)
    assert "Kafka" in profile.skills

    profile = h_engine.execute(profile)
    assert "Distributed Systems" in profile.hidden_skills

def test_counterfactual():
    engine = CounterfactualEngine()
    r1 = RankingDecision(
        candidate_id="c1", job_id="j1", overall_score=0.8,
        technical_fit=1.0, career_fit=0.5, behavior_fit=0.5, culture_fit=0.5,
        risk_score=0.1, strengths=[], weaknesses=[], evidence=[], missing_skills=[]
    )
    r2 = RankingDecision(
        candidate_id="c2", job_id="j1", overall_score=0.9,
        technical_fit=0.5, career_fit=1.0, behavior_fit=1.0, culture_fit=1.0,
        risk_score=0.0, strengths=[], weaknesses=[], evidence=[], missing_skills=[]
    )

    # Prioritize technical fit
    weights = {"technical": 0.8, "career": 0.1, "behavior": 0.05, "culture": 0.05, "risk_penalty": 0.1}
    ranked = engine.execute([r1, r2], weights)

    # c1 has better technical fit, should win
    assert ranked[0].candidate_id == "c1"
