import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.chat_router import router as chat_router
from app.routers.upload_router import router as upload_router
from app.utils.constants import BASE_DIR, CHROMA_DB_DIR, LOG_DIR, UPLOAD_DIR

app = FastAPI(title="Adaptive Multi-Model RAG Assistant")

app.mount(
    "/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/")
def index():
    from fastapi.responses import FileResponse

    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))


@app.on_event("startup")
def startup():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
