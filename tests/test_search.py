from src.search import build_answer, rank_segments


def test_rank_segments_returns_matching_evidence():
    segments = [
        {"start_seconds": 0, "end_seconds": 10, "text": "Python uses variables and functions."},
        {"start_seconds": 10, "end_seconds": 20, "text": "A database stores structured records."},
    ]

    results = rank_segments("How does Python use functions?", segments)

    assert len(results) == 1
    assert results[0]["start_seconds"] == 0


def test_answer_explains_when_no_evidence_is_found():
    assert "could not find" in build_answer("weather", []).lower()

