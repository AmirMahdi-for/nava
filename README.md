# 🎧 Nava – Real-Time AI Voice Assistant  
A FastAPI-based real-time voice assistant that supports:  
- Audio → Text (Speech-to-Text)  
- Smart conversation using OpenAI LLM  
- Text → Audio (Text-to-Speech)  
- Bi-directional WebSocket streaming  

Nava is designed for ultra-low-latency voice communication powered by OpenAI.

---

## 📌 Features
- 🔊 **Real-time WebSocket voice streaming**
- 🎙️ **Speech-to-Text using Whisper**
- 🤖 **Conversational AI using OpenAI LLMs**
- 🔈 **Text-to-Speech output (mp3)**
- 📡 **Chunked binary audio streaming support**
- 📝 Centralized structured logging with Loguru
- 🔧 Fully Dockerized (Dockerfile included)

---

## 🧱 Tech Stack
- **Python 3.11+**
- **FastAPI**
- **WebSockets**
- **OpenAI SDK**
- **SQLAlchemy (async) + Alembic**
- **Loguru**
- **Docker**

---

## ⚙️ Environment Variables (`.env`)
Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_key_here
ENVIRONMENT=development
PROJECT_NAME=nava
VERSION=0.1.0
WEBSOCKET_MAX_SIZE=10000000
LOG_LEVEL=DEBUG
```

---

## 📦 Installation (Local Development)

### 1️⃣ Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

docker build -t nava .

http://127.0.0.1:8000
```
---

## 🔌 WebSocket Usage Example (CLI)
### Send WAV → Receive MP3

```
cat hello.wav | websocat -b --no-close \
  ws://127.0.0.1:8000/api/v1/ws/voice \
  > answer.mp3

```
---
## 🧠 How the Pipeline Works

1. Client sends audio bytes

2. Server transcribes using Whisper

3. LLM generates conversational response

4. Server sends back text

5. TTS generates audio reply

6. Audio is streamed back to the client

---

## 🗂 Logs

### Log files stored in:

```
logs/app.log

```

---

## 📄 License

MIT License – Free for personal and commercial use.