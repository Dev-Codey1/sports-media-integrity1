from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.core.config import settings


class WatermarkService:
    def apply_visible_watermark(self, source_path: str, label: str | None = None) -> str:
        text = label or settings.default_visible_watermark
        image = Image.open(source_path).convert("RGBA")
        overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        font = ImageFont.load_default()
        width, height = image.size
        draw.text((width * 0.05, height * 0.9), text, fill=(255, 255, 255, 120), font=font)
        watermarked = Image.alpha_composite(image, overlay).convert("RGB")
        out_path = Path(settings.watermark_dir) / f"wm_{Path(source_path).name}"
        watermarked.save(out_path)
        return str(out_path)

    def meta_seal_status(self) -> dict:
        return {
            "enabled": settings.enable_meta_seal_adapter,
            "status": "adapter-only",
            "note": "Replace this hook with real Meta Seal inference worker in production.",
        }

    def video_seal_status(self) -> dict:
        return {
            "enabled": settings.enable_video_seal_adapter,
            "status": "adapter-only",
            "note": "Replace this hook with real VideoSeal pipeline in production.",
        }
