from __future__ import annotations

from datetime import datetime, timezone
from app.utils.files import json_dump


class ProvenanceService:
    def build_manifest(self, *, asset_sha256: str, owner: str, title: str, asset_type: str, league: str | None) -> str:
        manifest = {
            "version": "1.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "asset": {
                "title": title,
                "type": asset_type,
                "sha256": asset_sha256,
            },
            "issuer": {
                "owner": owner,
                "league": league,
                "claim": "Official sports media asset registration",
            },
            "verification": {
                "method": "local provenance manifest",
                "future_upgrade": "C2PA / signed credentials / external registry",
            },
        }
        return json_dump(manifest)
