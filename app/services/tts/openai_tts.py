from openai import AsyncOpenAI
from app.core.config import settings
from app.core.logging import logger

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def synthesize(text: str) -> bytes:

    try:
        response = await client.audio.speech.create(
            model="tts-1-hd",
            voice="nova",  # alloy, echo, fable, onyx, nova, shimmer
            input=text.strip(),
            response_format="mp3"
        )
        audio_bytes = response.content 
        if not audio_bytes:
            raise ValueError("TTS response خالی بود")
        logger.success(f"TTS → {len(audio_bytes)/1024:.1f} KB صدا تولید شد")
        return audio_bytes
    except Exception as e:
        logger.error(f"خطا در TTS: {e}")
        raise