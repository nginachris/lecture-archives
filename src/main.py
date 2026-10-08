from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from .db import create_lecture, get_lecture, initialize
from .schemas import LectureCreate, SearchRequest
from .search import build_answer, rank_segments


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize()
    yield


app = FastAPI(title="LectureLens API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/lectures", status_code=201)
def add_lecture(lecture: LectureCreate):
    lecture_id = create_lecture(
        lecture.title,
        [segment.model_dump() for segment in lecture.segments],
    )
    return {"id": lecture_id, "title": lecture.title, "status": "ready"}


@app.get("/lectures/{lecture_id}")
def lecture_details(lecture_id: int):
    lecture = get_lecture(lecture_id)
    if lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture


@app.post("/lectures/{lecture_id}/search")
def search_lecture(lecture_id: int, request: SearchRequest):
    lecture = get_lecture(lecture_id)
    if lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found")

    evidence = rank_segments(request.question, lecture["segments"], request.limit)
    return {
        "lecture_id": lecture_id,
        "question": request.question,
        "answer": build_answer(request.question, evidence),
        "evidence": evidence,
    }

