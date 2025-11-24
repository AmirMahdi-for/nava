from openai import AsyncOpenAI
from app.core.config import settings
from app.core.logging import logger

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_response(text: str, history: list[dict]) -> str:
    messages = [{"role": "system", "content": "تو یک دستیار صوتی فارسی به نام نوا هستی. کوتاه، مفید و دوستانه جواب بده."}]
    messages.extend(history)
    messages.append({"role": "user", "content": text})

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    content = response.choices[0].message.content
    logger.info(f"LLM Response: {content[:60]}...")
    return content