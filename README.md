# Sports Media Guardian AI (Winning Upgrade)

A hackathon-ready, GitHub-ready backend for protecting the integrity of digital sports media.

This upgraded version adds:
- multi-signal image matching,
- semantic embedding fallback layer,
- video keyframe analysis,
- provenance manifest generation,
- explainable incident scoring,
- benchmark endpoint,
- discovery provider abstraction,
- watermark adapter hooks for Meta Seal / VideoSeal / Watermark Anything / AudioSeal.

## Why judges will care
This is not only a copy detector. It is an **authenticity + propagation intelligence** system.

## Feature highlights
- Register official images/videos.
- Generate hashes and local features.
- Apply visible watermark.
- Build provenance manifests.
- Upload suspicious media or suspicious URLs.
- Run similarity matching across official assets.
- Create explainable incidents with recommended actions.
- Benchmark robustness across edited variants.

## Quick start
```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open docs:
```bash
http://127.0.0.1:8000/docs
```

## Demo flow
1. Register an official asset using `/api/v1/assets/register`
2. Upload suspicious evidence using `/api/v1/scans/upload-evidence`
3. Match the evidence using `/api/v1/scans/match-evidence/{evidence_id}`
4. Review incidents via `/api/v1/incidents`
5. Run `/api/v1/benchmarks/asset/{asset_id}` to show robustness story

## Endpoints overview

### Assets
- `POST /api/v1/assets/register`
- `GET /api/v1/assets`
- `GET /api/v1/assets/{asset_id}`

### Evidence / scanning
- `POST /api/v1/scans/upload-evidence`
- `POST /api/v1/scans/ingest-url`
- `POST /api/v1/scans/match-evidence/{evidence_id}`
- `GET /api/v1/scans/evidence`

### Incidents
- `GET /api/v1/incidents`
- `GET /api/v1/incidents/{incident_id}`

### Dashboard
- `GET /api/v1/dashboard/summary`

### Benchmarks
- `POST /api/v1/benchmarks/asset/{asset_id}`

## Important honesty note
This repo contains a strong, working core engine. Fully internet-wide scanning needs external feeds, search providers, or platform APIs. The codebase is already structured for that using provider adapters.

## Real-world inspiration
OpenCV's `img_hash` module exists specifically for image hashing and large-scale similar-image retrieval, while Meta's open-source watermarking tools such as VideoSeal and Meta Seal strengthen robust authentication and attribution workflows. citeturn999326search0turn999326search2turn999326search1

## Folder structure
```text
sports-media-guardian-v2/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
├── scripts/
├── sample_data/
├── data/
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── ARCHITECTURE.md
```
