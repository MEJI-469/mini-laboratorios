"""
Ejecuta TODO el Lab 2 desde aquí:
- Parte A: módulo suelto (modulo_cadenas)
- Parte B: paquete textkit (importaciones absolutas y relativas)
"""

from __future__ import annotations
from pprint import pprint

# === Parte A: módulo ===
import modulo_cadenas as mc

# === Parte B: paquete con importación ABSOLUTA (desde __init__.py) ===
from textkit import normalize as pkg_normalize, slugify as pkg_slugify
from textkit import is_slug as pkg_is_slug, require_non_empty as pkg_require_non_empty

# También una importación ABSOLUTA a un submódulo específico:
import textkit.validators as validators


def demo_parte_a():
    print("\n=== PARTE A — MÓDULO 'modulo_cadenas' ===")
    texto = "  ¡Hola Mundo Ágil!  "
    print("normalizar:", mc.normalizar(texto))
    print("slugify:", mc.slugify(texto))

    s_ok = "hola-mundo-agil"
    s_bad = "Hola Mundo!!!"

    print("es_slug(s_ok):", mc.es_slug(s_ok))
    print("es_slug(s_bad):", mc.es_slug(s_bad))

    # Caso límite (error controlado)
    try:
        mc.requerir_no_vacio("    ")
    except ValueError as e:
        print("requerir_no_vacio('    ') -> ERROR esperado:", e)


def demo_parte_b():
    print("\n=== PARTE B — PAQUETE 'textkit' ===")

    # Usando API pública reexportada por __init__.py (importación absoluta)
    texto = "  Programación en PYTHON — Módulos y Paquetes  "
    print("pkg_normalize:", pkg_normalize(texto))
    slug = pkg_slugify(texto)
    print("pkg_slugify:", slug)
    print("pkg_is_slug(slug):", pkg_is_slug(slug))

    # Caso límite (error controlado)
    try:
        pkg_require_non_empty("   ")
    except ValueError as e:
        print("require_non_empty('   ') -> ERROR esperado:", e)

    # Importación ABSOLUTA a submódulo (validators) y uso
    print("validators.is_slug('mi-slug-valid'):", validators.is_slug("mi-slug-valid"))


def main():
    demo_parte_a()
    demo_parte_b()
    print("\n✅ Lab 2 ejecutado correctamente.")


if __name__ == "__main__":
    main()
