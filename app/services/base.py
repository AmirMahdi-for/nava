from abc import ABC, abstractmethod
from typing import Protocol

class STTService(Protocol):
    async def transcribe(self, audio_bytes: bytes) -> str: ...

class LLMService(Protocol):
    async def generate_response(self, text: str, history: list[dict]) -> str: ...

class TTSService(Protocol):
    async def synthesize(self, text: str) -> bytes: ...