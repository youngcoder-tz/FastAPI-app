from transformers import pipeline
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        self.nlp = pipeline("sentiment-analysis", 
                          model="cardiffnlp/twitter-roberta-base-sentiment")
        
    def analyze_text(self, text: str) -> dict:
        # Hybrid analysis approach
        ml_result = self.nlp(text)[0]
        blob_result = TextBlob(text)
        
        return {
            "ml_sentiment": ml_result["label"],
            "ml_score": ml_result["score"],
            "polarity": blob_result.sentiment.polarity,
            "subjectivity": blob_result.sentiment.subjectivity
        }

    def analyze_complaints_batch(self, complaints: list[str]) -> pd.DataFrame:
        """Batch process for performance"""
        return pd.DataFrame([
            self.analyze_text(complaint) 
            for complaint in complaints
        ])