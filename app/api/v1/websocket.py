from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from app.core.logging import logger
from app.services.stt.openai_stt import transcribe
from app.services.llm.openai_llm import generate_response
from app.services.tts.openai_tts import synthesize

router = APIRouter()


@router.websocket("/ws/voice")
async def websocket_voice_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")

    conversation_history = []

    try:
        while True:
            data = await websocket.receive_bytes()
            logger.debug(f"Received audio chunk: {len(data)} bytes")

            user_text = await transcribe(data)
            await websocket.send_json({"type": "transcription", "text": user_text})

            conversation_history.append({"role": "user", "content": user_text})

            bot_response = await generate_response(user_text, conversation_history)
            conversation_history.append({"role": "assistant", "content": bot_response})

            await websocket.send_json({"type": "bot_text", "text": bot_response})

            audio_bytes = await synthesize(bot_response)
            await websocket.send_bytes(audio_bytes)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.exception(f"Error in websocket: {e}")
        await websocket.send_json({"type": "error", "message": "خطا در پردازش صدا"})
    finally:
        await websocket.close()