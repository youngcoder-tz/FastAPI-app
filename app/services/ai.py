from transformers import pipeline
import numpy as np

class AIService:
    def __init__(self):
        # Initialize models
        self.classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased",
            top_k=3
        )
        self.similarity_model = pipeline(
            "feature-extraction",
            model="sentence-transformers/all-MiniLM-L6-v2"
        )

    def categorize_complaint(self, text: str):
        results = self.classifier(text)
        return [{"label": r["label"], "score": r["score"]} for r in results]

    def predict_promise_fulfillment(self, promise_text: str, history: str):
        embeddings = self.similarity_model([promise_text, history])
        similarity = np.dot(embeddings[0], embeddings[1])
        return {
            "similarity_score": float(similarity),
            "prediction": "likely" if similarity > 0.7 else "unlikely"
        }

ai_service = AIService()



# from functools import lru_cache
# from redis import Redis
# import json
# from datetime import timedelta

# class CachedAIService:
#     def __init__(self, redis: Redis):
#         self.redis = redis
#         self.cache_ttl = timedelta(hours=1)

#     @lru_cache(maxsize=1000)
#     def _cached_classification(self, text: str):
#         # Actual model inference
#         return self.classifier(text)

#     def categorize_complaint(self, text: str):
#         # Redis caching layer
#         cache_key = f"ai:cat:{hash(text)}"
#         cached = self.redis.get(cache_key)
        
#         if cached:
#             return json.loads(cached)
        
#         # Model inference
#         result = self._cached_classification(text)
        
#         # Cache results
#         self.redis.setex(
#             cache_key,
#             self.cache_ttl,
#             json.dumps(result)
#         )
#         return result