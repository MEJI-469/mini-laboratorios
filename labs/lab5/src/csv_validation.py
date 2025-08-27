from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple, Iterable

REQUIRED_COLUMNS = ["id", "name", "age", "score"]

@dataclass
class ValidationResult:
    rows: int
    errors: List[str]

def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    """
    Lee un CSV con encabezado y devuelve lista de dicts (valores en str).
    """
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def validate_header(row_keys: Iterable[str]) -> List[str]:
    """
    Valida que todas las columnas requeridas estén presentes.
    """
    keys = set(row_keys)
    missing = [c for c in REQUIRED_COLUMNS if c not in keys]
    return [f"Falta columna obligatoria: {c}" for c in missing]

def validate_types_and_rules(rows: List[Dict[str, str]]) -> List[str]:
    """
    Reglas mínimas:
    - id entero, único y >= 1
    - name no vacío
    - age entero >= 0
    - score float >= 0
    """
    errors: List[str] = []
    seen_ids = set()

    for idx, row in enumerate(rows, start=1):
        loc = f"(fila {idx})"

        # id
        try:
            _id = int(row["id"])
            if _id < 1:
                errors.append(f"{loc} id debe ser >= 1")
        except Exception:
            errors.append(f"{loc} id no es entero válido: {row.get('id')!r}")
            _id = None

        if _id is not None:
            if _id in seen_ids:
                errors.append(f"{loc} id duplicado: {_id}")
            seen_ids.add(_id)

        # name
        name = (row.get("name") or "").strip()
        if name == "":
            errors.append(f"{loc} name vacío")

        # age
        try:
            age = int(row["age"])
            if age < 0:
                errors.append(f"{loc} age negativo: {age}")
        except Exception:
            errors.append(f"{loc} age no es entero válido: {row.get('age')!r}")

        # score
        try:
            score = float(row["score"])
            if score < 0:
                errors.append(f"{loc} score negativo: {score}")
        except Exception:
            errors.append(f"{loc} score no es float válido: {row.get('score')!r}")

    return errors

def validate_csv(path: Path) -> ValidationResult:
    rows = read_csv_rows(path)
    header_errors = validate_header(rows[0].keys() if rows else REQUIRED_COLUMNS)
    data_errors = validate_types_and_rules(rows)
    return ValidationResult(rows=len(rows), errors=header_errors + data_errors)
