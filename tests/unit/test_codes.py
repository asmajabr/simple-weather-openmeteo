# tests/unit/test_codes.py

# Local
from src.helpers import code_to_text

def test_code_to_text_known_codes():
    assert code_to_text(0) == "Clear"
    assert code_to_text(1) == "Mainly clear"
    assert code_to_text(2) == "Partly cloudy"
    assert code_to_text(99) == "Thunderstorm with heavy hail"

