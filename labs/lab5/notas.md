# Lab 5 — Pytest + Módulo simple y CSV (Python 3.12)

## Parte A — Módulo `textutils`
**Funciones:**
- `normalize_spaces(s: str) -> str`: colapsa espacios y recorta.
- `word_count(s: str) -> int`: cuenta palabras tras normalizar.
- `is_palindrome(s: str, ignore_case=True, ignore_spaces=True) -> bool`: palíndromo flexible.

**Pruebas (`tests/test_textutils.py`):**
- Casos correctos, vacíos y errores de tipo (TypeError).

## Parte B — CSV con `csv`
**Dataset:** `labs/lab5/data/sample.csv` (generado automáticamente si no existe).
**Reglas de validación:**
- Columnas obligatorias: `id, name, age, score`.
- `id`: entero, único, >= 1.
- `name`: no vacío.
- `age`: entero >= 0.
- `score`: float >= 0.

**Pruebas (`tests/test_csv_validation.py`):**
- Dataset válido (sin errores).
- Dataset inválido (múltiples errores detectados).

## Cómo ejecutar
```bash
# Ejecutar todo el lab desde un solo main
python labs/lab5/src/main.py

# Correr pruebas
pytest -q

# (opcional) Solo este lab:
pytest -q labs/lab5/tests
