"""
Punto de entrada del paquete `textkit`.
Reexporta funciones clave para una API pública simple.
"""

from .cleaners import normalize, slugify
from .validators import is_slug, require_non_empty

__all__ = ["normalize", "slugify", "is_slug", "require_non_empty"]
