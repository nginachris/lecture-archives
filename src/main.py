from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from .db import create_lecture, create_upload, get_lecture, get_upload, initialize
from .schemas import LectureCreate, SearchRequest
from .search import build_answer, rank_segments
from .uploads import save_upload


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize()
    yield


app = FastAPI(title="LectureLens API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/uploads", status_code=201)
def upload_lecture(title: str = Form(...), file: UploadFile = File(...)):
    try:
        original_name, file_path = save_upload(file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    upload_id = create_upload(title, original_name, file_path)
    return {
        "id": upload_id,
        "title": title,
        "filename": original_name,
        "status": "uploaded",
    }


@app.get("/uploads/{upload_id}")
def upload_status(upload_id: int):
    upload = get_upload(upload_id)
    if upload is None:
        raise HTTPException(status_code=404, detail="Upload not found")
    return upload


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
