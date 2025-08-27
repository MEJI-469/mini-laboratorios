"""
textkit.validators – validadores y precondiciones.
Demuestra importación *relativa* desde otro módulo del mismo paquete.
"""

from __future__ import annotations
import re
from .cleaners import normalize  # <— importación relativa

__all__ = ["is_slug", "require_non_empty"]

_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def is_slug(s: str) -> bool:
    """Valida si 's' es un slug válido."""
    return bool(_SLUG.fullmatch(s))


def require_non_empty(s: str) -> str:
    """Exige que el texto no sea vacío (tras normalize + strip)."""
    if not isinstance(s, str):
        raise TypeError("require_non_empty() espera un str")
    if normalize(s) == "":
        raise ValueError("El texto no debe ser vacío")
    return s
