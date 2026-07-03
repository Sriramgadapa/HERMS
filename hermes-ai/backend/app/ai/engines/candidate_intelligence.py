from app.ai.base import CognitiveEngine
from app.domain.models import CandidateProfile, Experience
import json
import uuid

class CandidateIntelligenceEngine(CognitiveEngine):
    """
    2. Candidate Intelligence Engine (The Resume Deep-Reader)
    Parses candidate raw data/JSON into CandidateProfiles.
    """
    def execute(self, raw_candidate: dict) -> CandidateProfile:
        # Mock logic mapping raw JSON to schema
        skills = raw_candidate.get("skills", [])
        exp_data = raw_candidate.get("experience", [])
        experiences = [
            Experience(
                title=e.get("title", ""),
                company=e.get("company", ""),
                duration_months=e.get("duration_months", 12),
                description=e.get("description", "")
            )
            for e in exp_data
        ]

        return CandidateProfile(
            id=raw_candidate.get("id", str(uuid.uuid4())),
            name=raw_candidate.get("name", "Unknown Candidate"),
            skills=skills,
            experience=experiences,
            education=raw_candidate.get("education", [])
        )
