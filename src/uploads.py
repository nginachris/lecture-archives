import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = Path(__file__).resolve().parents[1] / "data" / "uploads"
ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".m4a", ".mov", ".wav", ".webm"}


def clean_filename(filename: str) -> str:
    name = Path(filename).name
    return re.sub(r"[^a-zA-Z0-9._-]", "_", name)


def save_upload(file: UploadFile) -> tuple[str, str]:
    original_name = clean_filename(file.filename or "lecture-upload")
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(f"Unsupported file type. Use one of: {allowed}")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid4().hex}{extension}"
    destination = UPLOAD_DIR / stored_name
    with destination.open("wb") as output:
        while chunk := file.file.read(1024 * 1024):
            output.write(chunk)

    return original_name, str(destination)
