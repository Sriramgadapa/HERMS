from app.ai.base import CognitiveEngine
from app.domain.models import JobProfile, CandidateProfile

class CultureTeamFitEngine(CognitiveEngine):
    """
    9. Culture & Team Fit Engine (The HR Partner)
    Aligns candidate soft skills with job business intent.
    """
    def execute(self, job: JobProfile, candidate: CandidateProfile) -> float:
        # Mock logic based on behavioral expectations vs signals
        if not candidate.behavioral_signals:
            return 0.5

        # Combine engagement and responsiveness for a proxy culture fit
        sig = candidate.behavioral_signals
        score = (sig.engagement_score * 0.5) + (sig.responsiveness * 0.5)
        return round(score, 2)
