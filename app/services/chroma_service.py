import chromadb

from app.utils.constants import CHROMA_DB_DIR, COLLECTION_NAME

_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)


def _get_collection():
    return _client.get_or_create_collection(COLLECTION_NAME)


def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
    ids: list[str] = None,
):
    collection = _get_collection()
    if ids is None:
        import uuid

        ids = [f"chunk_{uuid.uuid4()}" for _ in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def delete_chunks(ids: list[str]):
    collection = _get_collection()
    if ids:
        collection.delete(ids=ids)


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


def get_chunks_by_file_names(file_names: list[str], limit: int = 3):
    collection = _get_collection()
    if not file_names:
        return [], []

    # ChromaDB supports $in operator for lists
    if len(file_names) == 1:
        where_filter = {"file_name": file_names[0]}
    else:
        where_filter = {"file_name": {"$in": file_names}}

    results = collection.get(
        where=where_filter, limit=limit, include=["documents", "metadatas"]
    )

    docs = results.get("documents", []) if results.get("documents") else []
    metas = results.get("metadatas", []) if results.get("metadatas") else []
    return docs, metas
