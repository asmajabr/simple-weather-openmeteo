# tests/unit/test_codes.py

# Local
from src.helpers import code_to_text

def test_code_to_text_known_codes():
    assert code_to_text(0) == "Clear sky"
    assert code_to_text(1) == "Mainly clear"


def test_code_to_text_unknown():
    assert code_to_text(999).startswith("Unknown")
