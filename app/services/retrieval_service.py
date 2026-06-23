import os
import json
from app.utils.constants import BASE_DIR, TOP_K
from app.services.chroma_service import query_chunks, get_chunks_by_file_names
from app.services.embedding_service import generate_embedding

KNOWLEDGE_GRAPH_PATH = os.path.join(BASE_DIR, "db", "knowledge_graph.json")


def _load_knowledge_graph() -> dict:
    if os.path.exists(KNOWLEDGE_GRAPH_PATH):
        try:
            with open(KNOWLEDGE_GRAPH_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def retrieve(question: str) -> tuple[list[str], list[dict]]:
    """
    Link-Aware Retrieval:
    1. Perform initial vector search for the top K chunks.
    2. Check retrieved chunks for note links in the Knowledge Graph.
    3. Query ChromaDB for chunks of those linked notes.
    4. Combine and deduplicate chunks for a richer context.
    """
    # 1. Base vector search
    try:
        q_emb = generate_embedding(question)
        docs, metas = query_chunks(q_emb, top_k=TOP_K)
    except Exception as e:
        print(f"Error during base retrieval query: {e}")
        return [], []

    combined_docs = []
    combined_metas = []
    seen_docs = set()

    for d, m in zip(docs, metas):
        if d not in seen_docs:
            seen_docs.add(d)
            combined_docs.append(d)
            combined_metas.append(m)

    # 2. Extract links from knowledge graph
    kg = _load_knowledge_graph()
    linked_files = []

    for m in metas:
        if m.get("source_type") == "obsidian":
            file_name = m.get("file_name", "")
            note_name = os.path.splitext(file_name)[0]
            
            # Fetch links from KG
            links = kg.get(note_name, [])
            
            # Fallback to checking serialized links in the chunk metadata
            if not links and "links" in m:
                try:
                    links = json.loads(m["links"])
                except Exception:
                    pass
            
            for link in links:
                linked_files.append(f"{link}.md")
                linked_files.append(f"{link}.markdown")

    # Deduplicate linked files
    linked_files = list(set(linked_files))

    # 3. Retrieve chunks for the linked files
    if linked_files:
        try:
            # Limit the expansion search to get a maximum of 5 expanded chunks
            linked_docs, linked_metas = get_chunks_by_file_names(linked_files, limit=5)
            for ld, lm in zip(linked_docs, linked_metas):
                if ld not in seen_docs:
                    seen_docs.add(ld)
                    combined_docs.append(ld)
                    combined_metas.append(lm)
        except Exception as e:
            print(f"Error retrieving linked chunks: {e}")

    return combined_docs, combined_metas
