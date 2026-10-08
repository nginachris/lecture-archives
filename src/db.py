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

