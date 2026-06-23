import os
import json
import uuid
from app.utils.constants import BASE_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from app.services.ingestion_service import extract_content
from app.services.embedding_service import generate_embedding
from app.services.chroma_service import store_chunks, delete_chunks

SYNC_STATE_PATH = os.path.join(BASE_DIR, "db", "sync_state.json")
KNOWLEDGE_GRAPH_PATH = os.path.join(BASE_DIR, "db", "knowledge_graph.json")


def _load_json(file_path: str) -> dict:
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_json(file_path: str, data: dict):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def sync_vault(vault_path: str) -> dict:
    """
    Recursively discovers markdown files in the specified vault path,
    performs incremental ingestion using timestamps, updates the Chroma database,
    and builds/updates the knowledge graph.
    """
    # Clean input path by removing surrounding whitespace and enclosing quotes
    clean_path = vault_path.strip().strip('"').strip("'")
    normalized_vault_path = os.path.abspath(clean_path)
    if not os.path.exists(normalized_vault_path):
        raise ValueError(f"Vault path does not exist: {normalized_vault_path}")

    sync_state = _load_json(SYNC_STATE_PATH)
    knowledge_graph = _load_json(KNOWLEDGE_GRAPH_PATH)

    visited_paths = set()
    notes_synced = 0
    chunks_indexed = 0
    step = CHUNK_SIZE - CHUNK_OVERLAP

    # Walk vault directory
    for root, _, files in os.walk(normalized_vault_path):
        for file in files:
            if file.lower().endswith((".md", ".markdown")):
                full_path = os.path.join(root, file)
                # Save relative path using forward slashes for cross-platform stability
                rel_path = os.path.relpath(full_path, normalized_vault_path).replace("\\", "/")
                note_name = os.path.splitext(file)[0]
                visited_paths.add(rel_path)

                try:
                    mtime = os.path.getmtime(full_path)
                except Exception:
                    continue

                stored_info = sync_state.get(rel_path, {})
                stored_mtime = stored_info.get("last_modified")

                if stored_mtime == mtime:
                    # Unmodified file, count current chunks
                    chunks_indexed += len(stored_info.get("chunk_ids", []))
                    continue

                # Modified or new file: delete old chunks first
                old_ids = stored_info.get("chunk_ids", [])
                if old_ids:
                    try:
                        delete_chunks(old_ids)
                    except Exception as e:
                        print(f"Error removing old chunks for {rel_path}: {e}")

                # Extract content and Obsidian links
                try:
                    content, links = extract_content(full_path)
                except Exception as e:
                    print(f"Error extracting content from {full_path}: {e}")
                    continue

                # Create text chunks
                if not content.strip():
                    file_chunks = [""]
                else:
                    file_chunks = [content[i:i + CHUNK_SIZE] for i in range(0, len(content), step)]

                # Generate embeddings & save to Chroma
                try:
                    embeddings = [generate_embedding(c) for c in file_chunks]
                except Exception as e:
                    print(f"Error generating embeddings for {full_path}: {e}")
                    continue

                chunk_ids = [f"obsidian_{uuid.uuid4()}" for _ in range(len(file_chunks))]
                
                # Setup rich metadata
                metadatas = [
                    {
                        "source_type": "obsidian",
                        "file_name": file,
                        "vault_path": rel_path,
                        "links": json.dumps(links)
                    }
                    for _ in file_chunks
                ]

                try:
                    store_chunks(file_chunks, embeddings, metadatas, chunk_ids)
                except Exception as e:
                    print(f"Error storing chunks in Chroma for {full_path}: {e}")
                    continue

                # Update state trackers
                sync_state[rel_path] = {
                    "last_modified": mtime,
                    "chunk_ids": chunk_ids
                }
                knowledge_graph[note_name] = links
                notes_synced += 1
                chunks_indexed += len(chunk_ids)

    # Clean up deleted files
    deleted_paths = set(sync_state.keys()) - visited_paths
    for del_path in deleted_paths:
        del_info = sync_state.get(del_path, {})
        old_ids = del_info.get("chunk_ids", [])
        if old_ids:
            try:
                delete_chunks(old_ids)
            except Exception as e:
                print(f"Error deleting chunks for deleted file {del_path}: {e}")

        if del_path in sync_state:
            del sync_state[del_path]

        file_name = os.path.basename(del_path)
        note_name = os.path.splitext(file_name)[0]
        if note_name in knowledge_graph:
            del knowledge_graph[note_name]

    # Save to disk
    _save_json(SYNC_STATE_PATH, sync_state)
    _save_json(KNOWLEDGE_GRAPH_PATH, knowledge_graph)

    return {
        "status": "success",
        "notes_synced": notes_synced,
        "chunks_indexed": chunks_indexed
    }


def get_vault_stats() -> dict:
    """Returns statistics about notes, chunks, links and embeddings in the vault."""
    sync_state = _load_json(SYNC_STATE_PATH)
    knowledge_graph = _load_json(KNOWLEDGE_GRAPH_PATH)

    notes = len(sync_state)
    chunks = sum(len(info.get("chunk_ids", [])) for info in sync_state.values())
    links = sum(len(links_list) for links_list in knowledge_graph.values())
    embeddings = chunks

    return {
        "notes": notes,
        "chunks": chunks,
        "links": links,
        "embeddings": embeddings
    }
