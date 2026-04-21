from __future__ import annotations

import json
from pathlib import Path
import cv2
import imagehash
import numpy as np
from PIL import Image
from app.utils.files import replace_ext


class FingerprintService:
    def _load_pil(self, path: str) -> Image.Image:
        return Image.open(path).convert("RGB")

    def _load_cv(self, path: str):
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"Could not read image: {path}")
        return img

    def _histogram_signature(self, image_bgr) -> list[float]:
        hist = cv2.calcHist([image_bgr], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return [round(float(x), 6) for x in hist.tolist()]

    def _orb_descriptors(self, image_bgr):
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create(nfeatures=500)
        keypoints, descriptors = orb.detectAndCompute(gray, None)
        if descriptors is None:
            descriptors = np.empty((0, 32), dtype=np.uint8)
        return keypoints, descriptors

    def _descriptor_path(self, image_path: str) -> str:
        return replace_ext(image_path, "_orb") + ".npy"

    def create_image_fingerprint(self, path: str) -> dict:
        pil = self._load_pil(path)
        image_bgr = self._load_cv(path)

        ahash = str(imagehash.average_hash(pil))
        dhash = str(imagehash.dhash(pil))
        phash = str(imagehash.phash(pil))
        colorhash = str(imagehash.colorhash(pil))
        histogram = self._histogram_signature(image_bgr)
        _, descriptors = self._orb_descriptors(image_bgr)
        descriptor_path = self._descriptor_path(path)
        np.save(descriptor_path, descriptors)

        return {
            "ahash": ahash,
            "dhash": dhash,
            "phash": phash,
            "colorhash": colorhash,
            "histogram_signature": json.dumps(histogram),
            "orb_descriptor_path": descriptor_path,
        }

    def compare_hash(self, left_hex: str | None, right_hex: str | None, bits: int = 16) -> float:
        if not left_hex or not right_hex:
            return 0.0
        left = imagehash.hex_to_hash(left_hex)
        right = imagehash.hex_to_hash(right_hex)
        distance = left - right
        return max(0.0, 1 - (distance / float(bits * bits)))

    def compare_histograms(self, left_json: str | None, right_json: str | None) -> float:
        if not left_json or not right_json:
            return 0.0
        left = np.array(json.loads(left_json), dtype=np.float32)
        right = np.array(json.loads(right_json), dtype=np.float32)
        similarity = cv2.compareHist(left, right, cv2.HISTCMP_CORREL)
        return float((similarity + 1) / 2)

    def compare_orb(self, left_path: str | None, right_path: str | None) -> float:
        if not left_path or not right_path:
            return 0.0
        if not Path(left_path).exists() or not Path(right_path).exists():
            return 0.0
        left = np.load(left_path)
        right = np.load(right_path)
        if len(left) == 0 or len(right) == 0:
            return 0.0
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(left, right)
        if not matches:
            return 0.0
        good = [m for m in matches if m.distance < 50]
        return min(1.0, len(good) / max(10, min(len(left), len(right))))
