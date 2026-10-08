from pydantic import BaseModel, Field


class TranscriptSegment(BaseModel):
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(ge=0)
    text: str = Field(min_length=1)


class LectureCreate(BaseModel):
    title: str = Field(min_length=1)
    segments: list[TranscriptSegment] = Field(min_length=1)


class SearchRequest(BaseModel):
    question: str = Field(min_length=1)
    limit: int = Field(default=3, ge=1, le=10)

