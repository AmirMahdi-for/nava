from openai import AsyncOpenAI
from app.core.config import settings
from app.core.logging import logger
import aiofiles
import tempfile
import os

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def transcribe(audio_bytes: bytes) -> str:

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    tmp_path = tmp_file.name
    tmp_file.close()  

    try:

        async with aiofiles.open(tmp_path, "wb") as f:
            await f.write(audio_bytes)

        with open(tmp_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,           
                response_format="text"
            )

        result = str(transcript).strip()
        if not result:
            logger.warning("Whisper چیزی تشخیص نداد")
            result = "سلام"

        logger.success(f"تشخیص گفتار: {result}")
        return result

    except Exception as e:
        logger.error(f"خطا در Whisper: {e}")
        raise
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass