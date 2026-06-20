from pydantic import BaseModel


class UploadResponse(BaseModel):
    status: str
    chunks_indexed: int
