from app.ai.base import CognitiveEngine
from app.domain.models import JobProfile
import uuid

class JobIntelligenceEngine(CognitiveEngine):
    """
    1. Job Intelligence Engine (The Requirements Analyst)
    Parses unstructured Job Descriptions into a structured JobProfile.
    """
    def execute(self, jd_text: str) -> JobProfile:
        # Mock logic for MVP: In reality, use an LLM (OpenAI/Anthropic) here
        jd_lower = jd_text.lower()
        skills = []
        if "python" in jd_lower: skills.append("Python")
        if "react" in jd_lower: skills.append("React")
        if "machine learning" in jd_lower or "ai" in jd_lower: skills.append("Machine Learning")
        if "fastapi" in jd_lower: skills.append("FastAPI")

        return JobProfile(
            id=str(uuid.uuid4()),
            role="Software Engineer (Inferred)",
            required_skills=skills,
            preferred_skills=["Docker", "AWS"],
            domain="Tech",
            experience_years_required=3,
            behavior_expectations={"leadership": "Medium", "autonomy": "High"}
        )
