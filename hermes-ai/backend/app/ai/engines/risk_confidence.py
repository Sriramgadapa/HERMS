from app.ai.base import CognitiveEngine
from app.domain.models import JobProfile, CandidateProfile

class RiskConfidenceEngine(CognitiveEngine):
    """
    7. Risk & Confidence Engine (The Skeptic)
    Flags anomalies, career gaps, or missing critical competencies.
    """
    def execute(self, job: JobProfile, candidate: CandidateProfile, tech_fit: float) -> float:
        # A higher score means HIGHER risk. We will return a normalized risk metric.
        risk = 0.0

        # Risk factor: Poor technical fit
        if tech_fit < 0.5:
            risk += 0.4

        # Risk factor: Job hopping (many short stints)
        short_stints = sum(1 for exp in candidate.experience if exp.duration_months < 12)
        if short_stints > 2:
            risk += 0.3

        return min(risk, 1.0)
