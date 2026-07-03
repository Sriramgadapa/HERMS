from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BehavioralSignal(BaseModel):
    engagement_score: float = Field(0.0, ge=0.0, le=1.0)
    responsiveness: float = Field(0.0, ge=0.0, le=1.0)
    behavior_confidence: float = Field(0.0, ge=0.0, le=1.0)

class Experience(BaseModel):
    title: str
    company: str
    duration_months: int
    description: str = ""
    domain: Optional[str] = None

class Evidence(BaseModel):
    claim: str
    source: str
    confidence: float

class CandidateProfile(BaseModel):
    id: str
    name: str
    skills: List[str]
    hidden_skills: List[str] = []
    experience: List[Experience] = []
    education: List[str] = []
    behavioral_signals: Optional[BehavioralSignal] = None

class JobProfile(BaseModel):
    id: str
    role: str
    required_skills: List[str]
    preferred_skills: List[str] = []
    domain: Optional[str] = None
    experience_years_required: int = 0
    behavior_expectations: Dict[str, str] = {}

class RankingDecision(BaseModel):
    candidate_id: str
    job_id: str
    overall_score: float
    technical_fit: float
    career_fit: float
    behavior_fit: float
    culture_fit: float
    risk_score: float
    strengths: List[str]
    weaknesses: List[str]
    evidence: List[Evidence]
    missing_skills: List[str]
