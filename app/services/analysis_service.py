from __future__ import annotations

import json
from pathlib import Path
import cv2
import numpy as np


class AnalysisService:
    def transformation_hints(self, original_path: str, suspicious_path: str) -> dict:
        left = cv2.imread(original_path)
        right = cv2.imread(suspicious_path)
        if left is None or right is None:
            return {"hints": ["analysis_unavailable"]}

        lh, lw = left.shape[:2]
        rh, rw = right.shape[:2]
        hints = []

        if abs((lw / max(lh, 1)) - (rw / max(rh, 1))) > 0.15:
            hints.append("possible_crop_or_resize")
        if (lw, lh) != (rw, rh):
            hints.append("resolution_changed")

        left_blur = cv2.Laplacian(cv2.cvtColor(left, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        right_blur = cv2.Laplacian(cv2.cvtColor(right, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        if right_blur < left_blur * 0.7:
            hints.append("possible_blur_or_recompression")

        left_mean = np.mean(left)
        right_mean = np.mean(right)
        if abs(float(left_mean - right_mean)) > 18:
            hints.append("possible_contrast_or_color_edit")

        return {
            "hints": hints or ["minor_or_unknown_transformations"],
            "left_resolution": [int(lw), int(lh)],
            "right_resolution": [int(rw), int(rh)],
            "blur_variance": {
                "original": round(float(left_blur), 3),
                "suspicious": round(float(right_blur), 3),
            },
        }
