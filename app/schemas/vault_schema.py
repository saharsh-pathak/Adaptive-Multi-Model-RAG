from pydantic import BaseModel


class VaultSyncRequest(BaseModel):
    vault_path: str


class VaultSyncResponse(BaseModel):
    status: str
    notes_synced: int
    chunks_indexed: int


class VaultStatsResponse(BaseModel):
    notes: int
    chunks: int
    links: int
    embeddings: int
