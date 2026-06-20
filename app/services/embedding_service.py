import requests
from app.utils.constants import OLLAMA_BASE_URL, EMBEDDING_MODEL

generate_embedding = lambda text: requests.post(
    f"{OLLAMA_BASE_URL}/api/embeddings",
    json={"model": EMBEDDING_MODEL, "prompt": text}
).json()["embedding"]
