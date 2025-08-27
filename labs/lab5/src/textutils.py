from __future__ import annotations

def normalize_spaces(s: str) -> str:
    """
    Colapsa espacios múltiples, quita espacios al inicio/fin.
    """
    if not isinstance(s, str):
        raise TypeError("normalize_spaces() espera str")
    return " ".join(s.split())

def word_count(s: str) -> int:
    """
    Cuenta palabras separadas por espacio tras normalizar.
    """
    if not isinstance(s, str):
        raise TypeError("word_count() espera str")
    s = normalize_spaces(s)
    if s == "":
        return 0
    return len(s.split(" "))

def is_palindrome(s: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Determina si s es palíndromo.
    - ignore_case: ignora mayúsculas/minúsculas
    - ignore_spaces: ignora espacios
    """
    if not isinstance(s, str):
        raise TypeError("is_palindrome() espera str")
    t = s
    if ignore_spaces:
        t = "".join(t.split())
    if ignore_case:
        t = t.lower()
    return t == t[::-1]
