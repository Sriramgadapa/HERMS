from app.ai.base import CognitiveEngine
from app.domain.models import JobProfile, CandidateProfile, Evidence
from rapidfuzz import fuzz

class EvidenceValidationEngine(CognitiveEngine):
    """
    8. Evidence & Validation Engine (The Fact-Checker)
    Cross-references extracted skills against concrete project achievements.
    """
    def execute(self, job: JobProfile, candidate: CandidateProfile) -> list[Evidence]:
        evidences = []
        for skill in job.required_skills:
            found = False
            for exp in candidate.experience:
                if skill.lower() in exp.description.lower() or skill.lower() in exp.title.lower():
                    evidences.append(Evidence(
                        claim=f"Has experience with {skill}",
                        source=f"Experience at {exp.company}: {exp.title}",
                        confidence=0.9
                    ))
                    found = True
                    break
            if not found:
                # Check general skills
                for c_skill in candidate.skills + candidate.hidden_skills:
                    if fuzz.ratio(skill.lower(), c_skill.lower()) > 80:
                        evidences.append(Evidence(
                            claim=f"Lists {skill} as a skill",
                            source="Skills Section",
                            confidence=0.7
                        ))
                        break

        return evidences
