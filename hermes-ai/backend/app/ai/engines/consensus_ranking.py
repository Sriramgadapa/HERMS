from app.ai.base import CognitiveEngine
from app.domain.models import RankingDecision

class ConsensusRankingEngine(CognitiveEngine):
    """
    11. Consensus & Ranking Engine (The Hiring Manager)
    Aggregates multi-dimensional scores into a baseline weighted recommendation.
    """
    def execute(
        self, job_id: str, candidate_id: str,
        tech_fit: float, career_fit: float,
        behavior_fit: float, culture_fit: float, risk_score: float,
        strengths: list, weaknesses: list, evidence: list, missing_skills: list
    ) -> RankingDecision:

        # Default Weights
        base_score = (tech_fit * 0.4) + (career_fit * 0.2) + (behavior_fit * 0.2) + (culture_fit * 0.2)
        final_score = max(0.0, min(1.0, base_score - (risk_score * 0.1)))

        return RankingDecision(
            candidate_id=candidate_id,
            job_id=job_id,
            overall_score=final_score,
            technical_fit=tech_fit,
            career_fit=career_fit,
            behavior_fit=behavior_fit,
            culture_fit=culture_fit,
            risk_score=risk_score,
            strengths=strengths,
            weaknesses=weaknesses,
            evidence=evidence,
            missing_skills=missing_skills
        )
