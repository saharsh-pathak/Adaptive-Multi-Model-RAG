import os, uuid
from fastapi import APIRouter, UploadFile, File
from app.schemas.upload_schema import UploadResponse
from app.services.pdf_service import extract_text
from app.services.embedding_service import generate_embedding
from app.services.chroma_service import store_chunks
from app.utils.constants import UPLOAD_DIR, CHUNK_SIZE, CHUNK_OVERLAP

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.pdf")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)
    step = CHUNK_SIZE - CHUNK_OVERLAP
    chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), step)]
    store_chunks(chunks, [generate_embedding(c) for c in chunks], list(range(1, len(chunks) + 1)))

    return UploadResponse(status="success", chunks_indexed=len(chunks))
