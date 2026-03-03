from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=50)


class ChatResponse(BaseModel):
    reply: str
    red_flag: bool = False
    red_flag_message: str | None = None


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
