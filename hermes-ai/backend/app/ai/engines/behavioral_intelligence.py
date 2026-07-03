from app.ai.base import CognitiveEngine
from app.domain.models import CandidateProfile, BehavioralSignal
import random

class BehavioralIntelligenceEngine(CognitiveEngine):
    """
    4. Behavioral Intelligence Engine (The Behavioral Psychologist)
    Derives behavioral metrics from Redrob signals or mock metadata.
    """
    def execute(self, candidate: CandidateProfile, raw_signals: dict = None) -> CandidateProfile:
        # Mock signal generation if none provided
        if not raw_signals:
            raw_signals = {
                "engagement_score": round(random.uniform(0.6, 1.0), 2),
                "responsiveness": round(random.uniform(0.7, 1.0), 2),
                "behavior_confidence": round(random.uniform(0.5, 0.95), 2)
            }

        candidate.behavioral_signals = BehavioralSignal(**raw_signals)
        return candidate
