from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    page: int | None = None


class Metrics(BaseModel):
    retrieval_ms: float
    generation_ms: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    model: str
    metrics: Metrics
