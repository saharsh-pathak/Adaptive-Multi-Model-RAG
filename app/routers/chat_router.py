import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat_schema import ChatRequest, ChatResponse, Source, Metrics
from app.services.retrieval_service import retrieve
from app.services.ollama_service import generate, stream_generate, classify_question_complexity
from app.utils.constants import SIMPLE_GEN_MODEL, COMPLEX_GEN_MODEL

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
    
    # 1. Classify complexity & Route
    complexity = classify_question_complexity(request.question)
    model = COMPLEX_GEN_MODEL if complexity == "COMPLEX" else SIMPLE_GEN_MODEL
    
    # 2. Retrieve using Link-Aware Retrieval
    chunks, metadatas = retrieve(request.question)
    retrieval_ms = round((time.time() - t0) * 1000, 2)

    prompt = _build_prompt(request.question, chunks)

    # 3. Generate answer
    t1 = time.time()
    answer = generate(model, prompt)
    generation_ms = round((time.time() - t1) * 1000, 2)

    # 4. Map sources and deduplicate
    sources = []
    seen_sources = set()
    for m in metadatas:
        source_type = m.get("source_type", "pdf")
        file_name = m.get("file_name", "unknown")
        page = m.get("page")
        vault_path = m.get("vault_path")
        
        source_key = (source_type, file_name, page, vault_path)
        if source_key not in seen_sources:
            seen_sources.add(source_key)
            sources.append(Source(
                source_type=source_type,
                file_name=file_name,
                page=page,
                vault_path=vault_path
            ))

    return ChatResponse(
        answer=answer,
        sources=sources,
        model=model,
        metrics=Metrics(retrieval_ms=retrieval_ms, generation_ms=generation_ms),
    )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    # 1. Classify complexity & Route
    complexity = classify_question_complexity(request.question)
    model = COMPLEX_GEN_MODEL if complexity == "COMPLEX" else SIMPLE_GEN_MODEL
    
    # 2. Retrieve
    chunks, metadatas = retrieve(request.question)
    prompt = _build_prompt(request.question, chunks)
    
    # 3. Stream generation
    return StreamingResponse(stream_generate(model, prompt), media_type="text/event-stream")
