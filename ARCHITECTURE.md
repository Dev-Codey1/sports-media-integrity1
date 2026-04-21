# Sports Media Guardian AI — Winning-Level Architecture

## Product thesis
Sports organizations do not just need copy detection. They need:
1. source authentication,
2. robust attribution after edits,
3. scalable discovery,
4. explainable evidence,
5. action recommendations.

This system combines **fingerprinting**, **semantic similarity**, **watermark/provenance adapters**, **video keyframe analysis**, and **incident intelligence**.

## Core pipeline

### 1) Asset registration
- Store the uploaded official asset.
- Generate exact SHA-256.
- Generate perceptual fingerprints (aHash, dHash, pHash, ORB descriptors, color histogram).
- Optionally generate visible watermark derivative.
- Build provenance manifest.
- Store all metadata for future audits.

### 2) Discovery / evidence ingestion
Evidence can arrive from:
- manual upload,
- suspicious URL capture,
- platform adapters,
- keyword/domain watchlists,
- future reverse-image providers.

### 3) Multi-signal matching
Each candidate is matched against registered assets using:
- exact hash similarity,
- perceptual hash similarity,
- ORB local feature similarity,
- histogram similarity,
- semantic embedding similarity,
- watermark evidence,
- provenance evidence.

### 4) Video pipeline
For video assets or evidence:
- extract keyframes,
- fingerprint per frame,
- aggregate clip confidence,
- optionally inspect audio and OCR overlays in future versions.

### 5) Explainable scoring
The system outputs a structured scorecard:
- exact match score,
- perceptual score,
- feature match score,
- semantic score,
- watermark/provenance bonuses,
- transformation hints,
- final risk score,
- recommended action.

### 6) Incident intelligence
For strong matches the system creates incidents with:
- evidence reference,
- matched asset,
- explanation,
- severity,
- recommendation,
- timeline fields.

## Why this is stronger than a normal hackathon MVP
- It goes beyond simple hashing.
- It supports edited/re-encoded variants.
- It separates core engine from discovery providers.
- It is explainable to judges and legal teams.
- It has clear production extension points.

## Production upgrade path
- Replace SQLite with PostgreSQL.
- Replace local file storage with S3/GCS.
- Add Celery / RabbitMQ / Kafka workers.
- Add CLIP/ViT embedding backend.
- Add Meta Seal / VideoSeal / AudioSeal real inference workers.
- Add OCR/logo detection service.
- Add dashboard UI and notification channels.
