from datetime import datetime
from pydantic import BaseModel


class EvidenceOut(BaseModel):
    id: int
    source_label: str
    platform: str | None = None
    source_url: str | None = None
    file_path: str | None = None
    asset_type: str
    created_at: datetime

    class Config:
        from_attributes = True
