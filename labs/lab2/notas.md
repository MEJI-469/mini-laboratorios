# Lab 2 — Módulos y Paquetes

## Parte A — Módulo `modulo_cadenas.py`
**API pública**
- `normalizar(texto: str) -> str`: quita acentos, minúsculas, colapsa espacios.
- `slugify(texto: str, max_len: int = 60) -> str`: genera un slug seguro; lanza `ValueError` si queda vacío.
- `es_slug(texto: str) -> bool`: valida un slug simple `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- `requerir_no_vacio(texto: str) -> str`: valida no vacío; lanza `ValueError` con mensaje claro.

**¿Por qué módulo separado?**
- Cohesiona utilidades de texto comunes que pueden reutilizarse en otros labs/proyectos sin cargar dependencias externas.
- Facilita pruebas unitarias y mantiene responsabilidades acotadas.

**Caso límite probado**
- `requerir_no_vacio("   ")` → `ValueError` con mensaje claro.
- `slugify("!!!")` → `ValueError` si el texto queda vacío tras limpiar.

Referencias: *Python 3.12 Docs – Modules*

---

## Parte B — Paquete `textkit/`
**Estructura**
- `textkit/cleaners.py`: `normalize`, `slugify`
- `textkit/validators.py`: `is_slug`, `require_non_empty`
- `textkit/__init__.py`: reexporta `normalize`, `slugify`, `is_slug`, `require_non_empty`

**Importaciones**
- **Absolutas (recomendadas):** `from textkit import slugify` o `import textkit.validators as validators` (claridad, evitan ambigüedad).
- **Relativas (dentro del paquete):** en `validators.py` → `from .cleaners import normalize` (acopla explícitamente a su paquete).

**Qué expone `__init__.py` y por qué**
- Reexporta las funciones clave para ofrecer una **API pública simple** (`textkit.slugify`, etc.) sin obligar al consumidor a conocer la estructura interna de submódulos.

Criterios de aceptación: 
- Paquete con `__init__.py` y ≥2 módulos diferenciados.
- Probadas importaciones absolutas y relativas (ver `main.py`).

Referencias: *Python 3.12 Docs – Packages*
