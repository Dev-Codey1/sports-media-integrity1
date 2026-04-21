from __future__ import annotations

from pathlib import Path
import cv2
from app.services.embedding_service import EmbeddingService
from app.services.fingerprint_service import FingerprintService


class BenchmarkService:
    def __init__(self) -> None:
        self.fingerprint = FingerprintService()
        self.embedding = EmbeddingService()

    def _variant_paths(self, source_path: str) -> dict[str, str]:
        image = cv2.imread(source_path)
        if image is None:
            raise ValueError(f"Could not read image: {source_path}")
        stem = Path(source_path).stem
        parent = Path(source_path).parent
        variants = {}

        resized = cv2.resize(image, (max(64, image.shape[1] // 2), max(64, image.shape[0] // 2)))
        resized_path = parent / f"{stem}_bm_resize.jpg"
        cv2.imwrite(str(resized_path), resized)
        variants["resize"] = str(resized_path)

        blur = cv2.GaussianBlur(image, (9, 9), 0)
        blur_path = parent / f"{stem}_bm_blur.jpg"
        cv2.imwrite(str(blur_path), blur)
        variants["blur"] = str(blur_path)

        crop = image[0:int(image.shape[0] * 0.85), 0:int(image.shape[1] * 0.85)]
        crop_path = parent / f"{stem}_bm_crop.jpg"
        cv2.imwrite(str(crop_path), crop)
        variants["crop"] = str(crop_path)

        overlay = image.copy()
        cv2.putText(overlay, "REPOST", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        overlay_path = parent / f"{stem}_bm_overlay.jpg"
        cv2.imwrite(str(overlay_path), overlay)
        variants["text_overlay"] = str(overlay_path)

        return variants

    def run_image_benchmark(self, source_path: str) -> dict:
        baseline = self.fingerprint.create_image_fingerprint(source_path)
        baseline_embedding = self.embedding.create_image_embedding(source_path)
        variants = self._variant_paths(source_path)
        rows = []
        for name, path in variants.items():
            fp = self.fingerprint.create_image_fingerprint(path)
            emb = self.embedding.create_image_embedding(path)
            rows.append({
                "variant": name,
                "phash_similarity": round(self.fingerprint.compare_hash(baseline["phash"], fp["phash"]), 4),
                "orb_similarity": round(self.fingerprint.compare_orb(baseline["orb_descriptor_path"], fp["orb_descriptor_path"]), 4),
                "semantic_similarity": round(self.embedding.cosine_similarity(baseline_embedding, emb), 4),
            })
        return {"source": source_path, "results": rows}
