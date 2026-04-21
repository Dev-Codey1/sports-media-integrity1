from datetime import datetime
from pydantic import BaseModel


class AssetOut(BaseModel):
    id: int
    title: str
    asset_type: str
    owner: str
    league: str | None = None
    file_path: str
    watermarked_path: str | None = None
    sha256: str
    provenance_manifest: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
