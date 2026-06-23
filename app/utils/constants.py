import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "db", "chroma")
LOG_DIR = os.path.join(BASE_DIR, "logs")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = "nomic-embed-text"

SIMPLE_GEN_MODEL = "qwen3:4b"
COMPLEX_GEN_MODEL = "alibayram/Qwen3-30B-A3B-Instruct-2507:latest"
GEN_MODEL = SIMPLE_GEN_MODEL

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3

# Like a table name equivalent in ChromaDB.
COLLECTION_NAME = "vault_chunks"
