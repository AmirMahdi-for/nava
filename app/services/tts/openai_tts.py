from openai import AsyncOpenAI
from app.core.config import settings
from app.core.logging import logger
import tempfile
import os

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def synthesize(text: str) -> bytes:

    temp_file = None
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_path = temp_file.name
        temp_file.close()

        response = await client.audio.speech.create(
            model="tts-1-hd",
            voice="alloy",
            input=text.strip(),
            response_format="mp3"
        )
        response.stream_to_file(temp_path)

        with open(temp_path, "rb") as f:
            audio_bytes = f.read()

        if not audio_bytes or len(audio_bytes) < 100:
            raise ValueError("TTS response خالی بود")

        logger.success(f"TTS → {len(audio_bytes)/1024:.1f} KB صدا (MP3 با header کامل) تولید شد")
        return audio_bytes
    except Exception as e:
        logger.error(f"خطا در TTS: {e}")
        raise
    finally:

        if temp_file and os.path.exists(temp_path):
            os.unlink(temp_path)