from __future__ import annotations

from pathlib import Path
import cv2
from app.core.config import settings


class VideoService:
    def extract_keyframes(self, video_path: str, stride_seconds: int = 1, max_frames: int = 12) -> list[str]:
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fps = capture.get(cv2.CAP_PROP_FPS) or 25
        stride = max(1, int(fps * stride_seconds))
        frames = []
        index = 0
        saved = 0
        temp_dir = Path(settings.temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)

        while saved < max_frames:
            ok, frame = capture.read()
            if not ok:
                break
            if index % stride == 0:
                out_path = temp_dir / f"keyframe_{Path(video_path).stem}_{saved}.jpg"
                cv2.imwrite(str(out_path), frame)
                frames.append(str(out_path))
                saved += 1
            index += 1

        capture.release()
        return frames
