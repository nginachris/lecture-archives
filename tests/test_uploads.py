from pathlib import Path

from src.uploads import clean_filename


def test_clean_filename_removes_path_and_unsafe_characters():
    assert clean_filename("folder/my lecture?.mp4") == "my_lecture_.mp4"


def test_upload_extension_is_case_insensitive():
    assert Path(clean_filename("lecture.MP4")).suffix.lower() == ".mp4"
