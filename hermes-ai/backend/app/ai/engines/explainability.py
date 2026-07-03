from app.ai.base import CognitiveEngine
from app.domain.models import JobProfile, CandidateProfile
from rapidfuzz import fuzz

class ExplainabilityEngine(CognitiveEngine):
    """
    12. Explainability Engine (The Communicator)
    Generates "Why?", "Why Not?", and identifies missing skills.
    """
    def execute(self, job: JobProfile, candidate: CandidateProfile, tech_fit: float) -> dict:
        strengths = []
        weaknesses = []
        missing_skills = []

        all_c_skills = [s.lower() for s in candidate.skills + candidate.hidden_skills]

        for req_skill in job.required_skills:
            found = False
            for c_skill in all_c_skills:
                if fuzz.ratio(req_skill.lower(), c_skill) > 80:
                    found = True
                    break
            if not found:
                missing_skills.append(req_skill)

        if len(missing_skills) == 0:
            strengths.append("Matches all required skills")
        else:
            weaknesses.append(f"Missing core skills: {', '.join(missing_skills)}")

        if tech_fit > 0.8:
            strengths.append("Excellent technical alignment with the role")

        if candidate.hidden_skills:
            strengths.append(f"Strong inferred capabilities: {', '.join(candidate.hidden_skills)}")

        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "missing_skills": missing_skills
        }
