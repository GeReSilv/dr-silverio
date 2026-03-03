import json
import logging
import os
from collections.abc import AsyncGenerator

from groq import AsyncGroq

from .models import ChatMessage
from .prompts import build_system_prompt
from .rag import search
from .safety import check_red_flags

logger = logging.getLogger(__name__)

_client: AsyncGroq | None = None


def get_client() -> AsyncGroq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set")
        _client = AsyncGroq(api_key=api_key)
    return _client


MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_HISTORY = 20


async def chat_stream(
    message: str,
    history: list[ChatMessage],
) -> AsyncGenerator[str, None]:
    """Stream chat response as SSE events."""
    is_red_flag, red_flag_msg = check_red_flags(message)
    if is_red_flag and red_flag_msg:
        yield f"data: {json.dumps({'type': 'red_flag', 'content': red_flag_msg})}\n\n"

    rag_context = search(message)
    system_prompt = build_system_prompt(rag_context)

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-MAX_HISTORY:]:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": message})

    try:
        client = get_client()
        stream = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1500,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield f"data: {json.dumps({'type': 'content', 'content': delta.content})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    except Exception as e:
        logger.error(f"Groq API error: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': 'Erro ao contactar o serviço. Tenta novamente.'})}\n\n"


async def chat_sync(
    message: str,
    history: list[ChatMessage],
) -> tuple[str, bool, str | None]:
    """Non-streaming chat response."""
    is_red_flag, red_flag_msg = check_red_flags(message)

    rag_context = search(message)
    system_prompt = build_system_prompt(rag_context)

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-MAX_HISTORY:]:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": message})

    try:
        client = get_client()
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1500,
        )
        reply = response.choices[0].message.content or ""
        return reply, is_red_flag, red_flag_msg

    except Exception as e:
        logger.error(f"Groq API error: {e}")
        raise
