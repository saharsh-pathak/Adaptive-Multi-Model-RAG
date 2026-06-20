import requests
import json

from app.utils.constants import OLLAMA_BASE_URL


def generate(model: str, prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )
    response.raise_for_status()
    return response.json()["response"]


def stream_generate(model: str, prompt: str):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={"model": model, "prompt": prompt, "stream": True},
        stream=True,
    )
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            yield data.get("response", "")
            if data.get("done"):
                break
