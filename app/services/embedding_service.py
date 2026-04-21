from __future__ import annotations

import json
import cv2
import numpy as np


class EmbeddingService:
    """
    Lightweight semantic fallback.

    In a production build, replace this with OpenCLIP / SigLIP / ViT embeddings.
    This fallback uses image statistics and edge patterns so the scoring pipeline and
    API contract stay stable without heavyweight model downloads.
    """

    def create_image_embedding(self, path: str) -> str:
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Could not read image: {path}")
        image = cv2.resize(image, (128, 128))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)
        edge_hist = np.histogram(edges, bins=16, range=(0, 256))[0].astype(np.float32)
        color_hist = []
        for channel in range(3):
            hist = cv2.calcHist([image], [channel], None, [16], [0, 256]).flatten().astype(np.float32)
            color_hist.extend(hist.tolist())
        vector = np.concatenate([edge_hist, np.array(color_hist, dtype=np.float32)])
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return json.dumps([round(float(x), 8) for x in vector.tolist()])

    def cosine_similarity(self, left_json: str | None, right_json: str | None) -> float:
        if not left_json or not right_json:
            return 0.0
        left = np.array(json.loads(left_json), dtype=np.float32)
        right = np.array(json.loads(right_json), dtype=np.float32)
        if left.size == 0 or right.size == 0:
            return 0.0
        denom = np.linalg.norm(left) * np.linalg.norm(right)
        if denom == 0:
            return 0.0
        return float(np.dot(left, right) / denom)
