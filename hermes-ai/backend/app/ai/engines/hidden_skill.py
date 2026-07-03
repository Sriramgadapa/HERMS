from app.ai.base import CognitiveEngine
from app.domain.models import CandidateProfile
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class HiddenSkillInferenceEngine(CognitiveEngine):
    """
    3. Hidden Skill Inference Engine (The Technical Expert)
    Infers missing abstract skills from explicit concrete skills.
    """
    def __init__(self):
        # MVP Mock logic for fast startup. In production, load actual model.
        # self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.skill_map = {
            "Distributed Systems": ["Kafka", "Redis", "Docker", "Kubernetes", "gRPC"],
            "Retrieval AI": ["FAISS", "Embeddings", "Vector Search", "Sentence Transformers"],
            "Full Stack": ["React", "FastAPI", "Node.js", "SQL"]
        }

    def execute(self, candidate: CandidateProfile) -> CandidateProfile:
        inferred = []
        c_skills_lower = [s.lower() for s in candidate.skills]

        for hidden_skill, indicators in self.skill_map.items():
            match_count = sum(1 for ind in indicators if ind.lower() in c_skills_lower)
            # If they have 2 or more indicator skills, infer the hidden skill
            if match_count >= 2:
                inferred.append(hidden_skill)

        candidate.hidden_skills = inferred
        return candidate
