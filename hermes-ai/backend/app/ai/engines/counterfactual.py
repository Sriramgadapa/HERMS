from app.ai.base import CognitiveEngine
from app.domain.models import RankingDecision
from typing import Dict, List

class CounterfactualEngine(CognitiveEngine):
    """
    10. Counterfactual Engine (The Strategist)
    Allows real-time re-ranking when priority weights change.
    """
    def execute(self, rankings: List[RankingDecision], weights: Dict[str, float]) -> List[RankingDecision]:
        # weights = {"technical": 0.4, "career": 0.2, "behavior": 0.2, "culture": 0.2, "risk_penalty": 0.1}

        for ranking in rankings:
            t = ranking.technical_fit * weights.get("technical", 0.4)
            c = ranking.career_fit * weights.get("career", 0.2)
            b = ranking.behavior_fit * weights.get("behavior", 0.2)
            cu = ranking.culture_fit * weights.get("culture", 0.2)

            base_score = t + c + b + cu
            risk_penalty = ranking.risk_score * weights.get("risk_penalty", 0.1)

            ranking.overall_score = max(0.0, min(1.0, base_score - risk_penalty))

        return sorted(rankings, key=lambda r: r.overall_score, reverse=True)
