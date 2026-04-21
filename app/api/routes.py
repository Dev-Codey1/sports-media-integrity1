from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.models.entities import Asset, Evidence, Incident
from app.schemas.asset import AssetOut
from app.schemas.evidence import EvidenceOut
from app.schemas.incident import IncidentOut
from app.services.benchmark_service import BenchmarkService
from app.services.discovery_service import DiscoveryService
from app.services.embedding_service import EmbeddingService
from app.services.fingerprint_service import FingerprintService
from app.services.match_service import MatchService
from app.services.provenance_service import ProvenanceService
from app.services.video_service import VideoService
from app.services.watermark_service import WatermarkService
from app.utils.files import json_dump, replace_ext, save_upload, sha256_file

router = APIRouter()

fingerprint_service = FingerprintService()
embedding_service = EmbeddingService()
watermark_service = WatermarkService()
provenance_service = ProvenanceService()
match_service = MatchService()
video_service = VideoService()
benchmark_service = BenchmarkService()
discovery_service = DiscoveryService()


def _store_media_fingerprints(model, path: str, asset_type: str) -> None:
    model.sha256 = sha256_file(path)
    if asset_type == "image":
        fp = fingerprint_service.create_image_fingerprint(path)
        model.ahash = fp["ahash"]
        model.dhash = fp["dhash"]
        model.phash = fp["phash"]
        model.colorhash = fp["colorhash"]
        model.histogram_signature = fp["histogram_signature"]
        model.orb_descriptor_path = fp["orb_descriptor_path"]
        model.semantic_signature = embedding_service.create_image_embedding(path)
    elif asset_type == "video":
        keyframes = video_service.extract_keyframes(path)
        if not keyframes:
            raise HTTPException(status_code=400, detail="No keyframes could be extracted from video.")
        representative = keyframes[0]
        fp = fingerprint_service.create_image_fingerprint(representative)
        model.ahash = fp["ahash"]
        model.dhash = fp["dhash"]
        model.phash = fp["phash"]
        model.colorhash = fp["colorhash"]
        model.histogram_signature = fp["histogram_signature"]
        model.orb_descriptor_path = fp["orb_descriptor_path"]
        model.semantic_signature = embedding_service.create_image_embedding(representative)
        model.analysis_json = json_dump({"keyframes": keyframes}) if hasattr(model, "analysis_json") else None
    else:
        raise HTTPException(status_code=400, detail="Only image and video are supported in this MVP.")


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    asset_count = db.query(Asset).count()
    evidence_count = db.query(Evidence).count()
    incident_count = db.query(Incident).count()
    high_risk = db.query(Incident).filter(Incident.severity.in_(["high", "critical"])).count()
    return {
        "assets": asset_count,
        "evidence": evidence_count,
        "incidents": incident_count,
        "high_risk_incidents": high_risk,
        "engine": {
            "semantic_backend": settings.embedding_backend,
            "provenance_enabled": settings.enable_provenance,
            "meta_seal": watermark_service.meta_seal_status(),
            "video_seal": watermark_service.video_seal_status(),
        },
    }


@router.post("/assets/register", response_model=AssetOut)
def register_asset(
    title: str = Form(...),
    asset_type: str = Form(...),
    owner: str = Form(...),
    league: str | None = Form(None),
    visible_watermark: bool = Form(False),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    path = save_upload(settings.upload_dir, file)
    asset = Asset(
        title=title,
        asset_type=asset_type,
        owner=owner,
        league=league,
        file_path=path,
        metadata_json=json_dump({"original_filename": file.filename}),
    )
    _store_media_fingerprints(asset, path, asset_type)
    if visible_watermark and asset_type == "image":
        asset.watermarked_path = watermark_service.apply_visible_watermark(path, f"{owner} | {league or 'Official'}")
    if settings.enable_provenance:
        asset.provenance_manifest = provenance_service.build_manifest(
            asset_sha256=asset.sha256,
            owner=owner,
            title=title,
            asset_type=asset_type,
            league=league,
        )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.get("/assets", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return db.query(Asset).order_by(Asset.created_at.desc()).all()


@router.get("/assets/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("/scans/upload-evidence", response_model=EvidenceOut)
def upload_evidence(
    source_label: str = Form(...),
    platform: str | None = Form(None),
    asset_type: str = Form("image"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    path = save_upload(settings.upload_dir, file)
    evidence = Evidence(
        source_label=source_label,
        platform=platform,
        file_path=path,
        asset_type=asset_type,
    )
    _store_media_fingerprints(evidence, path, asset_type)
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


@router.post("/scans/ingest-url")
def ingest_url(source_url: str = Form(...), platform: str | None = Form(None)):
    return discovery_service.ingest_url(source_url, platform)


@router.get("/scans/evidence", response_model=list[EvidenceOut])
def list_evidence(db: Session = Depends(get_db)):
    return db.query(Evidence).order_by(Evidence.created_at.desc()).all()


@router.post("/scans/match-evidence/{evidence_id}")
def match_evidence(evidence_id: int, db: Session = Depends(get_db)):
    evidence = db.get(Evidence, evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    assets = db.query(Asset).all()
    if not assets:
        raise HTTPException(status_code=400, detail="No registered assets found")

    results = []
    for asset in assets:
        if asset.asset_type != evidence.asset_type:
            continue
        comparison = match_service.compare(asset, evidence)
        results.append(comparison)
        if comparison["final_score"] >= settings.incident_threshold:
            incident = Incident(
                asset_id=asset.id,
                evidence_id=evidence.id,
                confidence_score=comparison["final_score"],
                severity=comparison["severity"],
                recommendation=comparison["recommendation"],
                title=f"Possible unauthorized use of {asset.title}",
                explanation_json=json_dump(comparison),
                transformation_summary=", ".join(comparison["transformations"].get("hints", [])),
                flagged=True,
            )
            db.add(incident)
    db.commit()
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return {
        "evidence_id": evidence_id,
        "matches_found": len(results),
        "top_matches": results[:5],
    }


@router.get("/incidents", response_model=list[IncidentOut])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.created_at.desc()).all()


@router.get("/incidents/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post("/benchmarks/asset/{asset_id}")
def benchmark_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.asset_type != "image":
        raise HTTPException(status_code=400, detail="Current benchmark endpoint supports image assets only")
    return benchmark_service.run_image_benchmark(asset.file_path)
