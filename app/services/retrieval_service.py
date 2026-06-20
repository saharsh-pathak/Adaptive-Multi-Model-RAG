from app.services.embedding_service import generate_embedding
from app.services.chroma_service import query_chunks
from app.utils.constants import TOP_K

retrieve = lambda q: query_chunks(generate_embedding(q), top_k=TOP_K)
