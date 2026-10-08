import json
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "data" / "lecturelens.db"


def connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def initialize() -> None:
    with connection() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS lectures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                transcript TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                status TEXT NOT NULL,
                error TEXT
            )
            """
        )


def create_lecture(title: str, segments: list[dict]) -> int:
    with connection() as db:
        cursor = db.execute(
            "INSERT INTO lectures (title, transcript) VALUES (?, ?)",
            (title, json.dumps(segments)),
        )
        return int(cursor.lastrowid)


def get_lecture(lecture_id: int) -> dict | None:
    with connection() as db:
        row = db.execute(
            "SELECT id, title, transcript FROM lectures WHERE id = ?",
            (lecture_id,),
        ).fetchone()

    if row is None:
        return None
    return {"id": row["id"], "title": row["title"], "segments": json.loads(row["transcript"])}


def create_upload(title: str, filename: str, file_path: str) -> int:
    with connection() as db:
        cursor = db.execute(
            "INSERT INTO uploads (title, filename, file_path, status) VALUES (?, ?, ?, ?)",
            (title, filename, file_path, "uploaded"),
        )
        return int(cursor.lastrowid)


def get_upload(upload_id: int) -> dict | None:
    with connection() as db:
        row = db.execute(
            "SELECT id, title, filename, status, error FROM uploads WHERE id = ?",
            (upload_id,),
        ).fetchone()

    if row is None:
        return None
    return dict(row)
