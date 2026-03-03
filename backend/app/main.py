import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from .chat import chat_stream, chat_sync
from .models import ChatRequest, ChatResponse, HealthResponse
from .rag import load_knowledge_base

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Dr. Silvério API",
    description="Assistente educativo de fisiologia e saúde",
    version="0.1.0",
)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logger.info("Loading knowledge base...")
    load_knowledge_base()
    logger.info("Dr. Silvério API ready")


@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse()


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Non-streaming chat endpoint."""
    reply, is_red_flag, red_flag_msg = await chat_sync(
        request.message, request.history
    )
    return ChatResponse(
        reply=reply,
        red_flag=is_red_flag,
        red_flag_message=red_flag_msg,
    )


@app.post("/api/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Streaming chat endpoint (SSE)."""
    return StreamingResponse(
        chat_stream(request.message, request.history),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
