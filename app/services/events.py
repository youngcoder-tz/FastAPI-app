import redis
from contextlib import asynccontextmanager

class EventProducer:
    def __init__(self):
        self.redis = redis.Redis(host='redis', port=6379, decode_responses=True)

    async def publish(self, channel: str, event: dict):
        self.redis.publish(channel, json.dumps(event))

    @asynccontextmanager
    async def subscribe(self, channel: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        try:
            yield pubsub
        finally:
            await pubsub.unsubscribe(channel)

event_producer = EventProducer()



class TownHallManager:
    def analyze_public_questions(self, transcript: str) -> dict:
        """Process live event transcripts"""
        questions = self._extract_questions(transcript)
        categorized = self._categorize_questions(questions)
        
        return {
            "top_topics": get_top_topics(categorized),
            "sentiment": self.sentiment_analyzer.analyze_text(transcript),
            "emerging_issues": detect_new_issues(categorized)
        }
    
    def generate_live_report(self, event_id: UUID) -> str:
        """Real-time HTML report for officials"""
        event = get_event_data(event_id)
        analysis = self.analyze_public_questions(event.transcript)
        
        return render_template(
            "townhall_report.html",
            top_questions=analysis["top_topics"],
            sentiment=analysis["sentiment"],
            wordcloud=generate_wordcloud(event.transcript)
        )