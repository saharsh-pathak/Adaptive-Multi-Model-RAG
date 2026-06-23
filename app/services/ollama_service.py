import requests
import json
from app.utils.constants import OLLAMA_BASE_URL, SIMPLE_GEN_MODEL, COMPLEX_GEN_MODEL


def classify_question_complexity(question: str) -> str:
    """
    Heuristically categorizes the query's complexity.
    RAG, comparison, architecture, and multi-step reasoning questions route to the
    larger model. Short factual questions stay on the smaller model.
    """
    normalized = " ".join(question.lower().split())

    complex_markers = (
        "rag",
        "retrieval augmented generation",
        "compare",
        "difference",
        "differences",
        "why",
        "how",
        "explain",
        "analyze",
        "analysis",
        "architecture",
        "design",
        "pipeline",
        "workflow",
        "tradeoff",
        "trade-offs",
        "debug",
        "optimize",
        "implementation",
        "implement",
        "multi-step",
        "synthesize",
        "synthesis",
    )

    if any(marker in normalized for marker in complex_markers):
        return "COMPLEX"

    if len(normalized.split()) > 18:
        return "COMPLEX"

    return "SIMPLE"


def generate(model: str, prompt: str) -> str:
    """
    Sends a generation request to Ollama. Falls back to SIMPLE_GEN_MODEL if the requested
    model (e.g. COMPLEX_GEN_MODEL) is not available or encounters an error.
    """
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
        )
        if response.status_code == 404 and model == COMPLEX_GEN_MODEL:
            print(f"Model {model} not found (404). Falling back to {SIMPLE_GEN_MODEL}.")
            return generate(SIMPLE_GEN_MODEL, prompt)
            
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        if model == COMPLEX_GEN_MODEL:
            print(f"Error calling model {model} ({e}). Falling back to {SIMPLE_GEN_MODEL}.")
            return generate(SIMPLE_GEN_MODEL, prompt)
        raise e


def stream_generate(model: str, prompt: str):
    """
    Streams generation results from Ollama. Falls back to SIMPLE_GEN_MODEL if the requested
    model is unavailable.
    """
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": model, "prompt": prompt, "stream": True},
            stream=True,
        )
        if response.status_code == 404 and model == COMPLEX_GEN_MODEL:
            print(f"Streaming: Model {model} not found. Falling back to {SIMPLE_GEN_MODEL}.")
            yield from stream_generate(SIMPLE_GEN_MODEL, prompt)
            return

        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                yield data.get("response", "")
                if data.get("done"):
                    break
    except Exception as e:
        if model == COMPLEX_GEN_MODEL:
            print(f"Streaming error calling {model} ({e}). Falling back to {SIMPLE_GEN_MODEL}.")
            yield from stream_generate(SIMPLE_GEN_MODEL, prompt)
        else:
            raise e
