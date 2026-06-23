import os
import uuid
from fastapi import APIRouter, UploadFile, File
from app.schemas.upload_schema import UploadResponse
from app.services.ingestion_service import extract_content
from app.services.embedding_service import generate_embedding
from app.services.chroma_service import store_chunks
from app.utils.constants import UPLOAD_DIR, CHUNK_SIZE, CHUNK_OVERLAP

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Retain the file extension so ingestion_service can identify the type
    _, ext = os.path.splitext(file.filename)
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text content
    text, _ = extract_content(file_path)
    
    # Chunk text
    step = CHUNK_SIZE - CHUNK_OVERLAP
    if not text.strip():
        chunks = [""]
    else:
        chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), step)]
        
    # Map metadata based on extension
    ext_lower = ext.lower()
    if ext_lower == ".pdf":
        source_type = "pdf"
    elif ext_lower in (".md", ".markdown"):
        source_type = "obsidian"
    else:
        source_type = "txt"

    metadatas = []
    for i in range(len(chunks)):
        meta = {
            "source_type": source_type,
            "file_name": file.filename
        }
        if source_type == "pdf":
            meta["page"] = i + 1
        metadatas.append(meta)

    # Embed and store chunks in Chroma
    embeddings = [generate_embedding(c) for c in chunks]
    store_chunks(chunks, embeddings, metadatas)

    return UploadResponse(status="success", chunks_indexed=len(chunks))
