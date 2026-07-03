from sqlalchemy import Column, Integer, String, Float, JSON
from .database import Base

class DBJob(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, index=True)
    role = Column(String, index=True)
    data = Column(JSON) # Store full JobProfile as JSON for MVP

class DBCandidate(Base):
    __tablename__ = "candidates"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    data = Column(JSON) # Store full CandidateProfile as JSON for MVP

class DBRanking(Base):
    __tablename__ = "rankings"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(String, index=True)
    candidate_id = Column(String, index=True)
    overall_score = Column(Float)
    data = Column(JSON) # Store full RankingDecision as JSON
