# mini-laboratorios
# Mini-Laboratorios – Guía de Ejecución

Este repositorio contiene 5 laboratorios de Python listos para ejecutarse **desde un `main.py`** (cuando aplica) y con pruebas automatizadas para los labs indicados.

---

## 🚀 Requisitos globales

- Python 3.11+ (recomendado 3.11 o 3.12)
- (Opcional) **GitHub Codespaces**: ya viene con Python y terminal integrados.
- Paquetes (instalados una vez en la raíz):
  ```bash
  pip install -r requirements.txt

# Lab 1
python labs/lab1/main.py

# Lab 2
python labs/lab2/main.py

# Lab 3
python labs/lab3/src/main.py
ruff check . && ruff format .
mypy labs/lab3/src
pytest -q labs/lab3/tests   # opcional

# Lab 4
python labs/lab4/main.py

# Lab 5
python labs/lab5/src/main.py
pytest -q labs/lab5/tests
