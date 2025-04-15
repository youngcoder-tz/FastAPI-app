import whisper
import asyncio
from pyarabic.araby import strip_tashkeel
from fastapi import HTTPException

class VoiceProcessor:
    def __init__(self):
        try:
            self.model = whisper.load_model("small")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Voice processing unavailable: {str(e)}"
            )

    async def process_voice_message(self, audio_path: str) -> dict:
        try:
            result = await asyncio.to_thread(self.model.transcribe, audio_path)
            return {
                "text": result["text"],
                "language": self._detect_language(result["text"]),
                "confidence": result.get("confidence", 0.8)
            }
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Voice processing failed: {str(e)}"
            )