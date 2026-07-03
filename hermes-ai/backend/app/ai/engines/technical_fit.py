from app.ai.base import CognitiveEngine
from app.domain.models import JobProfile, CandidateProfile
from rapidfuzz import fuzz

class TechnicalFitEngine(CognitiveEngine):
    """
    5. Technical & Domain Fit Engine (The Domain Specialist)
    Evaluates semantic match between JD skills and candidate skills (including hidden).
    """
    def execute(self, job: JobProfile, candidate: CandidateProfile) -> float:
        all_candidate_skills = candidate.skills + candidate.hidden_skills
        if not job.required_skills:
            return 1.0

        score_sum = 0
        for req_skill in job.required_skills:
            best_match = 0
            for c_skill in all_candidate_skills:
                match = fuzz.ratio(req_skill.lower(), c_skill.lower()) / 100.0
                if match > best_match:
                    best_match = match
            score_sum += best_match

        return score_sum / len(job.required_skills)
