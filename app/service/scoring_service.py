from __future__ import annotations


class ScoringService:
    def fuse(self, scorecard: dict) -> tuple[float, str, str]:
        score = (
            scorecard.get("sha256_exact", 0.0) * 0.35 +
            scorecard.get("phash_similarity", 0.0) * 0.15 +
            scorecard.get("ahash_similarity", 0.0) * 0.05 +
            scorecard.get("dhash_similarity", 0.0) * 0.05 +
            scorecard.get("colorhash_similarity", 0.0) * 0.05 +
            scorecard.get("histogram_similarity", 0.0) * 0.10 +
            scorecard.get("orb_similarity", 0.0) * 0.10 +
            scorecard.get("semantic_similarity", 0.0) * 0.15
        )
        score = max(0.0, min(1.0, score))

        if score >= 0.90:
            severity = "critical"
            recommendation = "Immediate takedown review"
        elif score >= 0.80:
            severity = "high"
            recommendation = "Human validation and takedown preparation"
        elif score >= 0.72:
            severity = "medium"
            recommendation = "Analyst review"
        elif score >= 0.60:
            severity = "low"
            recommendation = "Watchlist only"
        else:
            severity = "info"
            recommendation = "No action"

        return round(score, 4), severity, recommendation
