"""
Módulo de utilidades de cadenas (Parte A)
Funciones coherentes: normalizar, slugify, validar slug, requerir no vacío.
"""

from __future__ import annotations
import re
import unicodedata

__all__ = ["normalizar", "slugify", "es_slug", "requerir_no_vacio"]


def _quitar_acentos(texto: str) -> str:
    nfkd = unicodedata.normalize("NFD", texto)
    return "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")


def normalizar(texto: str) -> str:
    """
    - Quita acentos
    - Convierte a minúsculas
    - Colapsa espacios en uno solo
    - Elimina espacios al inicio/fin
    """
    if not isinstance(texto, str):
        raise TypeError("normalizar() espera un str")
    texto = _quitar_acentos(texto).lower().strip()
    texto = " ".join(texto.split())
    return texto


def slugify(texto: str, max_len: int = 60) -> str:
    """
    Convierte un texto en 'slug' (kebab-case):
    - normaliza (sin acentos, minúsculas)
    - reemplaza espacios/guiones bajos por '-'
    - remueve caracteres no alfanuméricos ni '-'
    - colapsa guiones repetidos y recorta a max_len
    - lanza ValueError si queda vacío
    """
    base = normalizar(texto)
    base = base.replace("_", "-").replace(" ", "-")
    base = re.sub(r"[^a-z0-9\-]", "", base)
    base = re.sub(r"-{2,}", "-", base).strip("-")
    if not base:
        raise ValueError("slugify(): el texto queda vacío tras limpiar")
    return base[:max_len]


_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def es_slug(texto: str) -> bool:
    """Valida si el texto cumple el patrón de slug simple."""
    return bool(_SLUG_RE.fullmatch(texto))


def requerir_no_vacio(texto: str) -> str:
    """
    Verifica que el string no esté vacío (tras strip()).
    Lanza ValueError con mensaje claro si no cumple.
    """
    if not isinstance(texto, str):
        raise TypeError("requerir_no_vacio() espera un str")
    if texto.strip() == "":
        raise ValueError("El texto no debe estar vacío")
    return texto
