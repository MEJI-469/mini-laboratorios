"""
textkit.cleaners – utilidades de limpieza/transformación de texto.
(Se usará importación relativa desde validators).
"""

from __future__ import annotations
import re
import unicodedata

__all__ = ["normalize", "slugify"]


def _strip_accents(s: str) -> str:
    nf = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in nf if unicodedata.category(ch) != "Mn")


def normalize(s: str) -> str:
    """Similar a normalizar(): sin acentos, minúsculas, espacios colapsados."""
    if not isinstance(s, str):
        raise TypeError("normalize() espera un str")
    s = _strip_accents(s).lower().strip()
    s = " ".join(s.split())
    return s


def slugify(s: str, max_len: int = 60) -> str:
    """Slug simple reutilizable en el paquete."""
    s = normalize(s)
    s = s.replace("_", "-").replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-]", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        raise ValueError("slugify(): quedó vacío")
    return s[:max_len]
