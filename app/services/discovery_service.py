from __future__ import annotations

from app.core.config import settings


class DiscoveryService:
    def ingest_url(self, url: str, platform: str | None = None) -> dict:
        return {
            "url": url,
            "platform": platform or self._guess_platform(url),
            "mode": "mock-adapter" if settings.enable_discovery_mock else "disabled",
            "status": "accepted",
            "note": "In production this is where reverse-image, social, and web discovery providers attach.",
        }

    def _guess_platform(self, url: str) -> str:
        for platform in ["instagram", "youtube", "x", "facebook", "telegram", "reddit"]:
            if platform in url.lower():
                return platform
        return "web"
