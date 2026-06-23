from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    source_type: str
    file_name: str
    page: int | None = None
    vault_path: str | None = None


class Metrics(BaseModel):
    retrieval_ms: float
    generation_ms: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    model: str
    metrics: Metrics
