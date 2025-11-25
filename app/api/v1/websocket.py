from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.logging import logger
from app.services.stt.openai_stt import transcribe
from app.services.llm.openai_llm import generate_response
from app.services.tts.openai_tts import synthesize
import asyncio

router = APIRouter()

CHUNK_GATHER_TIMEOUT = 0.25 

@router.websocket("/ws/voice")
async def websocket_voice_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")

    conversation_history = []

    try:
        while True:

            try:
                first_chunk = await asyncio.wait_for(websocket.receive_bytes(), timeout=30.0)
            except asyncio.TimeoutError:
                logger.warning("Timeout waiting for audio from client")
                break

            logger.debug(f"Received audio chunk: {len(first_chunk)} bytes (first)")

            audio_buf = bytearray()
            audio_buf.extend(first_chunk)

            while True:
                try:
                    chunk = await asyncio.wait_for(websocket.receive_bytes(), timeout=CHUNK_GATHER_TIMEOUT)
                    logger.debug(f"Received audio chunk: {len(chunk)} bytes (continuation)")
                    audio_buf.extend(chunk)
                except asyncio.TimeoutError:
                    break
                except WebSocketDisconnect:
                    logger.info("Client disconnected while sending audio")
                    break

            logger.info(f"Collected audio total: {len(audio_buf)} bytes — ارسال به STT...")

            try:
                user_text = await transcribe(bytes(audio_buf))
                logger.success(f"تشخیص گفتار: {user_text}")
                await websocket.send_json({"type": "transcription", "text": user_text})
            except Exception as e:
                logger.error(f"خطا در Whisper/STT: {e}")
                try:
                    await websocket.send_json({"type": "error", "message": "خطا در تشخیص گفتار: فرمت فایل نامعتبر یا ناقص است."})
                except:
                    pass
                continue

            try:
                conversation_history.append({"role": "user", "content": user_text})
                bot_response = await generate_response(user_text, conversation_history)
                conversation_history.append({"role": "assistant", "content": bot_response})
                await websocket.send_json({"type": "bot_text", "text": bot_response})
            except Exception as e:
                logger.exception(f"خطا در LLM: {e}")
                try:
                    await websocket.send_json({"type":"error","message":"خطا در تولید پاسخ"})
                except:
                    pass
                continue

            try:
                audio_bytes = await synthesize(bot_response)
                await websocket.send_bytes(audio_bytes)
                logger.success(f"صدا ارسال شد: {len(audio_bytes)} bytes")
            except Exception as e:
                logger.exception(f"خطا در TTS: {e}")
                try:
                    await websocket.send_json({"type":"error","message":"خطا در ساخت صدا"})
                except:
                    pass

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.exception(f"Unexpected error in websocket endpoint: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass
