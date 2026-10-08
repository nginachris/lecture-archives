# LectureLens

LectureLens is an AI study archive for recorded lectures and tutorials. Users will be able to upload a recording, ask questions about it, and receive answers with timestamped transcript evidence.

## MVP scope

The first version focuses on the core search workflow:

1. Store a lecture and its timestamped transcript segments.
2. Ask a natural-language question about the lecture.
3. Find the most relevant transcript segments.
4. Return an answer with evidence and timestamps.

Speech-to-text, user accounts, a web frontend, and generated flashcards will be added in later stages. Keeping the first version small makes it easier to test the search and evidence workflow before adding expensive video processing.

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

- `POST /lectures` creates a lecture with timestamped transcript segments.
- `GET /lectures/{lecture_id}` returns a lecture and its transcript.
- `POST /lectures/{lecture_id}/search` searches the lecture and returns matching evidence.

The current search uses a small, explainable keyword-ranking method. Later versions can replace it with embeddings and a language model while keeping the API contract similar.

## Roadmap

- Add video upload and background processing.
- Add local speech-to-text with Whisper.
- Add semantic search using embeddings.
- Generate answers from retrieved evidence.
- Add flashcards, quizzes, and study notes.
- Add a web dashboard and user authentication.

