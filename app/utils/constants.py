import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "db", "chroma")
LOG_DIR = os.path.join(BASE_DIR, "logs")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = "qwen3-embedding:4b"
GEN_MODEL = "qwen3:4b"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5

COLLECTION_NAME = "pdf_chunks"
