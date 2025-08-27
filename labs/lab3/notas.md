# Lab 3 — Codespaces, venv, ruff, mypy y pruebas

## Objetivos
- Usar Codespaces con entorno Python.
- Gestionar venv y `requirements.txt`.
- Ejecutar ruff (lint/format) y mypy (type checking).
- (Opcional) Correr pruebas con pytest.

## Estructura
- `labs/lab3/src/operaciones.py`: implementación con tipos y errores bien manejados.
- `labs/lab3/src/operaciones_buggy.py`: versión con tipos ausentes y retorno ambiguo (para mypy).
- `labs/lab3/src/main.py`: punto de entrada único del lab.
- `labs/lab3/tests/test_operaciones.py`: pruebas opcionales.

## Importante
- Ejecutar el lab: `python labs/lab3/src/main.py`
- Lint/format: `ruff check .` y `ruff format .`
- Type check: `mypy labs/lab3/src`
- Pruebas: `pytest -q`

## Decisiones
- Configuración centralizada en `pyproject.toml` (ruff y mypy) para todo el repo.
- Modo `strict` en mypy para detectar problemas de tipado.
- Caso límite documentado: división por cero -> `ValueError`.

## Referencias
- Codespaces, venv, pip, ruff, mypy, pytest (ver enunciado).


## (Para ver errores intencionales:)
- mypy labs/lab3/src/operaciones_buggy.py