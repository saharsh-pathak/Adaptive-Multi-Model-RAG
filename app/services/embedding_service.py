import requests

from app.utils.constants import EMBEDDING_MODEL, OLLAMA_BASE_URL


def generate_embedding(text):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embeddings",
        json={"model": EMBEDDING_MODEL, "prompt": text},
    )

    response.raise_for_status()

    return response.json()["embedding"]
