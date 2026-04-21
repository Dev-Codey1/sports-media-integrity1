from datetime import datetime
from pydantic import BaseModel


class IncidentOut(BaseModel):
    id: int
    asset_id: int
    evidence_id: int
    confidence_score: float
    severity: str
    recommendation: str
    title: str
    explanation_json: str
    transformation_summary: str | None = None
    flagged: bool
    created_at: datetime

    class Config:
        from_attributes = True
