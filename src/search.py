import re
from collections import Counter


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def rank_segments(question: str, segments: list[dict], limit: int = 3) -> list[dict]:
    question_words = set(tokenize(question))
    ranked = []

    for segment in segments:
        words = tokenize(segment["text"])
        matches = Counter(words) & Counter(question_words)
        score = sum(matches.values())
        if score:
            ranked.append({**segment, "score": score})

    ranked.sort(key=lambda item: (-item["score"], item["start_seconds"]))
    return ranked[:limit]


def build_answer(question: str, evidence: list[dict]) -> str:
    if not evidence:
        return "I could not find relevant evidence in this lecture."

    return "Based on the lecture: " + " ".join(item["text"] for item in evidence)

