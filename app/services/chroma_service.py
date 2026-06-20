import chromadb

from app.utils.constants import CHROMA_DB_DIR, COLLECTION_NAME


_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)


def _get_collection():
    return _client.get_or_create_collection(COLLECTION_NAME)


def store_chunks(chunks: list[str], embeddings: list[list[float]], sources: list[int]):
    collection = _get_collection()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"page": src} for src in sources]
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_chunks(embedding: list[float], top_k: int = 5):
    collection = _get_collection()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas"],
    )
    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []
    return docs, metas
