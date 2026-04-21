from __future__ import annotations

from app.services.analysis_service import AnalysisService
from app.services.embedding_service import EmbeddingService
from app.services.fingerprint_service import FingerprintService
from app.services.scoring_service import ScoringService
from app.utils.files import json_load


class MatchService:
    def __init__(self) -> None:
        self.fingerprint = FingerprintService()
        self.embedding = EmbeddingService()
        self.analysis = AnalysisService()
        self.scoring = ScoringService()

    def compare(self, asset, evidence) -> dict:
        scorecard = {
            "sha256_exact": 1.0 if asset.sha256 and evidence.sha256 and asset.sha256 == evidence.sha256 else 0.0,
            "ahash_similarity": self.fingerprint.compare_hash(asset.ahash, evidence.ahash),
            "dhash_similarity": self.fingerprint.compare_hash(asset.dhash, evidence.dhash),
            "phash_similarity": self.fingerprint.compare_hash(asset.phash, evidence.phash),
            "colorhash_similarity": self.fingerprint.compare_hash(asset.colorhash, evidence.colorhash) if asset.colorhash and evidence.colorhash else 0,
            "histogram_similarity": self.fingerprint.compare_histograms(asset.histogram_signature, evidence.histogram_signature),
            "orb_similarity": self.fingerprint.compare_orb(asset.orb_descriptor_path, evidence.orb_descriptor_path),
            "semantic_similarity": self.embedding.cosine_similarity(asset.semantic_signature, evidence.semantic_signature),
        }
        final_score, severity, recommendation = self.scoring.fuse(scorecard)
        transforms = self.analysis.transformation_hints(asset.file_path, evidence.file_path) if asset.file_path and evidence.file_path else {"hints": ["analysis_unavailable"]}

        return {
            "asset_id": asset.id,
            "evidence_id": evidence.id,
            "scorecard": scorecard,
            "final_score": final_score,
            "severity": severity,
            "recommendation": recommendation,
            "transformations": transforms,
        }
