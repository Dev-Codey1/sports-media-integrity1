from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    asset_type: Mapped[str] = mapped_column(String(50), index=True)
    owner: Mapped[str] = mapped_column(String(255), index=True)
    league: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_path: Mapped[str] = mapped_column(Text)
    watermarked_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    ahash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    dhash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    phash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    colorhash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    histogram_signature: Mapped[str | None] = mapped_column(Text, nullable=True)
    orb_descriptor_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    semantic_signature: Mapped[str | None] = mapped_column(Text, nullable=True)
    provenance_manifest: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_label: Mapped[str] = mapped_column(String(255), index=True)
    platform: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    asset_type: Mapped[str] = mapped_column(String(50), index=True)
    sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ahash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    dhash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    phash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    colorhash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    histogram_signature: Mapped[str | None] = mapped_column(Text, nullable=True)
    orb_descriptor_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    semantic_signature: Mapped[str | None] = mapped_column(Text, nullable=True)
    analysis_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[int] = mapped_column(Integer, index=True)
    evidence_id: Mapped[int] = mapped_column(Integer, index=True)
    confidence_score: Mapped[float] = mapped_column(Float, index=True)
    severity: Mapped[str] = mapped_column(String(50), index=True)
    recommendation: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    explanation_json: Mapped[str] = mapped_column(Text)
    transformation_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    flagged: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
