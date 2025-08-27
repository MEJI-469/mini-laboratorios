# Ajuste de ruta para importar desde labs/lab5/src sin packages
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from textutils import normalize_spaces, word_count, is_palindrome
import pytest

def test_normalize_spaces_basic():
    assert normalize_spaces("  hola   mundo  ") == "hola mundo"

def test_word_count():
    assert word_count("  hola   mundo  ") == 2
    assert word_count("") == 0

def test_is_palindrome_defaults():
    assert is_palindrome("Anita lava la tina")  # True con ignores por defecto
    assert not is_palindrome("hola")

def test_type_errors():
    with pytest.raises(TypeError):
        normalize_spaces(123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        word_count(None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        is_palindrome(3.14)  # type: ignore[arg-type]
