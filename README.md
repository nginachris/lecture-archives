# LectureLens

LectureLens is a small project for making recorded lectures easier to search. The idea is that a student can save a lecture, ask a question about it, and see which part of the transcript contains the answer.

## MVP scope

The first version keeps the workflow simple. It can:

1. Save a lecture and its transcript segments with timestamps.
2. Accept a question about the lecture.
3. Search the transcript for matching sections.
4. Return the matching text and its timestamp.

At the moment, transcript segments are entered directly through the API. Video upload and automatic transcription are planned for the next stages. Starting with the transcript search gives us something small that we can test before adding video processing.

## Planned architecture

```text
Lecture upload
      ↓
Background transcription job
      ↓
Timestamped transcript segments
      ↓
Search and retrieval
      ↓
Answer with source evidence
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API documentation.

## Current API

- `POST /uploads` accepts a lecture video or audio file and records it as an upload.
- `GET /uploads/{upload_id}` returns the current upload status.
- `POST /lectures` creates a lecture with timestamped transcript segments.
- `GET /lectures/{lecture_id}` returns a lecture and its transcript.
- `POST /lectures/{lecture_id}/search` searches the lecture and returns matching evidence.

The current search uses a small, explainable keyword-ranking method. Later versions can replace it with embeddings and a language model while keeping the API contract similar.

Uploads are currently stored locally and remain in the `uploaded` state. Automatic transcription is the next step.

## Roadmap

- Add video upload and background processing.
- Add local speech-to-text with Whisper.
- Add semantic search using embeddings.
- Generate answers from retrieved evidence.
- Add flashcards, quizzes, and study notes.
- Add a web dashboard and user authentication.

