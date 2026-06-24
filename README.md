# Adaptive Multi-Model RAG Assistant
<img width="959" height="539" alt="Screenshot 2026-06-23 173417" src="https://github.com/user-attachments/assets/2e042257-04cf-4e61-b778-55c5decdb958" />
<img width="959" height="539" alt="Screenshot 2026-06-23 174045" src="https://github.com/user-attachments/assets/dd0b043f-0f17-4070-96d9-057efb1158ea" />
<img width="959" height="539" alt="Screenshot 2026-06-23 174613" src="https://github.com/user-attachments/assets/91ad24ef-78c8-48f6-8a26-083535414898" />

Adaptive Multi-Model RAG Assistant is a fully local retrieval-augmented generation system built with FastAPI, ChromaDB, Ollama, and Obsidian vault integration.

It is designed to answer questions from multiple document sources while routing requests to different local models based on complexity:

- `qwen3:4b` for simpler, factual questions
- `alibayram/Qwen3-30B-A3B-Instruct-2507:latest` for deeper synthesis, comparison, and reasoning

This is not just a document search app. The retrieval layer is graph-aware, so when a relevant Obsidian note is found, the system also follows its `[[wikilinks]]` and pulls connected notes into context.

## What It Does

- Syncs an Obsidian vault from a local folder
- Ingests PDFs, Markdown files, and plain text files
- Chunks documents and stores embeddings in ChromaDB
- Retrieves relevant context for each question
- Expands retrieval through linked Obsidian notes
- Routes questions to a smaller or larger local model
- Returns answers with sources and timing metrics

## Why I Built It

I wanted a local-first RAG system that felt like a real backend project, not a notebook demo.

The focus here is on:

- proper FastAPI project structure
- local inference instead of cloud APIs
- retrieval that uses note relationships, not just vector similarity
- model routing that avoids using the largest model for every request

## Tech Stack

- FastAPI
- Uvicorn
- Ollama
- ChromaDB
- Pydantic
- PyPDF
- Requests

## Core Architecture

The backend is split into clean layers:

- `app/main.py` initializes the app and mounts routers
- `app/routers/` contains API endpoints
- `app/services/` contains ingestion, retrieval, embedding, and generation logic
- `app/utils/` contains shared constants and configuration
- `app/static/` contains the frontend UI

The main request flow is:

1. User enters a question in the UI
2. The app classifies the question as simple or complex
3. Retrieval fetches the most relevant chunks from ChromaDB
4. If the source is an Obsidian note, linked notes are expanded into the context
5. A prompt is built from the retrieved chunks
6. Ollama generates the final answer using the selected model

## Model Routing

The app uses two local models:

- `qwen3:4b` for short, direct questions
- `alibayram/Qwen3-30B-A3B-Instruct-2507:latest` for questions that involve:
  - comparison
  - explanation
  - architecture
  - analysis
  - multi-step reasoning
  - RAG-related queries

This keeps the system efficient for simple prompts while still allowing more capable reasoning when needed.

## Obsidian Graph-Aware Retrieval

The Obsidian sync is intentionally important.

When markdown notes are synced, the app extracts `[[wikilinks]]` and stores the relationships in a knowledge graph JSON file. During retrieval, if a relevant note is found, the system can expand context by pulling linked notes too.

That means the graph is part of retrieval, not just a visual feature.

## Repository Layout

```text
app/
  main.py
  routers/
  schemas/
  services/
  static/
  utils/
db/
vault/
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Ollama

Make sure Ollama is running locally.

### 3. Pull the models

```bash
ollama pull qwen3:4b
ollama pull alibayram/Qwen3-30B-A3B-Instruct-2507:latest
ollama pull nomic-embed-text
```

If you want to use a different Ollama host, set:

```bash
set OLLAMA_BASE_URL=http://localhost:11434
```

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## How To Use

### Sync an Obsidian vault

Enter the absolute path to your vault folder, for example:

```text
C:\Users\sahar\OneDrive\Desktop\MMRAG\vault
```

### Upload a file

Use the file ingestion panel to upload:

- `.pdf`
- `.md`
- `.markdown`
- `.txt`
- `.text`

### Ask a question

Type a question in the query console and the app will:

- retrieve relevant context
- choose the appropriate model
- generate an answer
- show the sources used

## API Endpoints

- `GET /`
- `POST /upload`
- `POST /chat`
- `POST /chat/stream`
- `POST /vault/sync`
- `GET /vault/stats`

## Notes

- This project is fully local and does not depend on external LLM APIs.
- ChromaDB persists embeddings locally under `db/chroma/`.
- Uploaded files and generated runtime data should stay out of version control.
- The app is intended for experimentation, demos, and practical local RAG workflows.

## Project Goal

The goal of this project is to show that a useful, structured RAG system can be built with open source models, local storage, and a clean backend architecture.

It is also a practical experiment in:

- local LLM inference
- adaptive model selection
- graph-aware context expansion
- document ingestion pipelines
- backend design with FastAPI

