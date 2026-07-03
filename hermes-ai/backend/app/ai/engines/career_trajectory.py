from app.ai.base import CognitiveEngine
from app.domain.models import JobProfile, CandidateProfile

class CareerTrajectoryEngine(CognitiveEngine):
    """
    6. Career Trajectory Engine (The Career Coach)
    Evaluates promotion velocity, domain loyalty, and relevant experience.
    """
    def execute(self, job: JobProfile, candidate: CandidateProfile) -> float:
        # Mock logic based on total experience years
        total_months = sum(exp.duration_months for exp in candidate.experience)
        total_years = total_months / 12.0

        req_years = job.experience_years_required
        if req_years == 0:
            return 1.0

        if total_years >= req_years:
            return 1.0
        else:
            return round(total_years / req_years, 2)
