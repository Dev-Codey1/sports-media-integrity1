from __future__ import annotations

import hashlib
import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile


def save_upload(upload_dir: str, file: UploadFile) -> str:
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename or "").suffix or ".bin"
    filename = f"{uuid.uuid4().hex}{ext}"
    path = Path(upload_dir) / filename
    with path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(path)


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_dump(data: dict | list) -> str:
    import json
    return json.dumps(data, ensure_ascii=False, indent=2)


def json_load(text: str | None):
    import json
    if not text:
        return None
    return json.loads(text)


def replace_ext(path: str, suffix: str) -> str:
    src = Path(path)
    return str(src.with_name(f"{src.stem}{suffix}{src.suffix}"))


def file_size_mb(path: str) -> float:
    return round(os.path.getsize(path) / (1024 * 1024), 4)
