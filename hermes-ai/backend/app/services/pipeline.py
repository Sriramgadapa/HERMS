from app.ai.engines.job_intelligence import JobIntelligenceEngine
from app.ai.engines.candidate_intelligence import CandidateIntelligenceEngine
from app.ai.engines.hidden_skill import HiddenSkillInferenceEngine
from app.ai.engines.behavioral_intelligence import BehavioralIntelligenceEngine
from app.ai.engines.technical_fit import TechnicalFitEngine
from app.ai.engines.career_trajectory import CareerTrajectoryEngine
from app.ai.engines.risk_confidence import RiskConfidenceEngine
from app.ai.engines.evidence_validation import EvidenceValidationEngine
from app.ai.engines.culture_fit import CultureTeamFitEngine
from app.ai.engines.consensus_ranking import ConsensusRankingEngine
from app.ai.engines.explainability import ExplainabilityEngine
from app.ai.engines.counterfactual import CounterfactualEngine

class HermesPipeline:
    def __init__(self):
        self.job_engine = JobIntelligenceEngine()
        self.candidate_engine = CandidateIntelligenceEngine()
        self.hidden_skill_engine = HiddenSkillInferenceEngine()
        self.behavior_engine = BehavioralIntelligenceEngine()
        self.tech_fit_engine = TechnicalFitEngine()
        self.career_engine = CareerTrajectoryEngine()
        self.risk_engine = RiskConfidenceEngine()
        self.evidence_engine = EvidenceValidationEngine()
        self.culture_engine = CultureTeamFitEngine()
        self.consensus_engine = ConsensusRankingEngine()
        self.explainability_engine = ExplainabilityEngine()
        self.counterfactual_engine = CounterfactualEngine()

    def analyze_job(self, jd_text: str):
        return self.job_engine.execute(jd_text)

    def process_candidate(self, raw_candidate: dict):
        profile = self.candidate_engine.execute(raw_candidate)
        profile = self.hidden_skill_engine.execute(profile)
        profile = self.behavior_engine.execute(profile)
        return profile

    def rank_candidate(self, job_profile, candidate_profile):
        tech_fit = self.tech_fit_engine.execute(job_profile, candidate_profile)
        career_fit = self.career_engine.execute(job_profile, candidate_profile)
        risk_score = self.risk_engine.execute(job_profile, candidate_profile, tech_fit)
        behavior_fit = candidate_profile.behavioral_signals.behavior_confidence if candidate_profile.behavioral_signals else 0.5
        culture_fit = self.culture_engine.execute(job_profile, candidate_profile)

        evidence = self.evidence_engine.execute(job_profile, candidate_profile)
        explanations = self.explainability_engine.execute(job_profile, candidate_profile, tech_fit)

        ranking = self.consensus_engine.execute(
            job_id=job_profile.id,
            candidate_id=candidate_profile.id,
            tech_fit=tech_fit,
            career_fit=career_fit,
            behavior_fit=behavior_fit,
            culture_fit=culture_fit,
            risk_score=risk_score,
            strengths=explanations["strengths"],
            weaknesses=explanations["weaknesses"],
            evidence=evidence,
            missing_skills=explanations["missing_skills"]
        )
        return ranking

pipeline = HermesPipeline()
