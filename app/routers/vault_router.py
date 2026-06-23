from fastapi import APIRouter, HTTPException
from app.schemas.vault_schema import VaultSyncRequest, VaultSyncResponse, VaultStatsResponse
from app.services.vault_service import sync_vault, get_vault_stats

router = APIRouter()


@router.post("/vault/sync", response_model=VaultSyncResponse)
def sync(request: VaultSyncRequest):
    try:
        res = sync_vault(request.vault_path)
        return VaultSyncResponse(
            status=res["status"],
            notes_synced=res["notes_synced"],
            chunks_indexed=res["chunks_indexed"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@router.get("/vault/stats", response_model=VaultStatsResponse)
def stats():
    try:
        res = get_vault_stats()
        return VaultStatsResponse(
            notes=res["notes"],
            chunks=res["chunks"],
            links=res["links"],
            embeddings=res["embeddings"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")
