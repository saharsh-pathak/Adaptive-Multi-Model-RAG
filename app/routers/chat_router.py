import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat_schema import ChatRequest, ChatResponse, Source, Metrics
from app.services.retrieval_service import retrieve
from app.services.ollama_service import generate, stream_generate
from app.utils.constants import GEN_MODEL

router = APIRouter()

_build_prompt = lambda q, chunks: f"""You are a helpful AI assistant. Use the following context to answer the question.

Context:
{"\n\n".join(chunks)}

Question:
{q}

Answer:"""


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    t0 = time.time()
    chunks, metadatas = retrieve(request.question)
    retrieval_ms = round((time.time() - t0) * 1000, 2)

    prompt = _build_prompt(request.question, chunks)

    t1 = time.time()
    answer = generate(GEN_MODEL, prompt)
    generation_ms = round((time.time() - t1) * 1000, 2)

    return ChatResponse(
        answer=answer,
        sources=[Source(page=m.get("page")) for m in metadatas if m.get("page")],
        model=GEN_MODEL,
        metrics=Metrics(retrieval_ms=retrieval_ms, generation_ms=generation_ms),
    )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    chunks, metadatas = retrieve(request.question)
    prompt = _build_prompt(request.question, chunks)
    return StreamingResponse(stream_generate(GEN_MODEL, prompt), media_type="text/event-stream")
