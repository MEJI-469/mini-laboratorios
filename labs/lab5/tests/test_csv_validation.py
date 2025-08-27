import sys, pathlib, csv
from typing import List, Dict

# Ruta a src
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from csv_validation import validate_csv  # type: ignore

def _write_csv(p: pathlib.Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        # encabezado vacío mínimo
        rows = [{"id": "1", "name": "a", "age": "0", "score": "0"}]
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def test_valid_dataset(tmp_path: pathlib.Path):
    p = tmp_path / "ok.csv"
    rows = [
        {"id": "1", "name": "Ana", "age": "20", "score": "10.5"},
        {"id": "2", "name": "Luis", "age": "0",  "score": "0"},
    ]
    _write_csv(p, rows)
    result = validate_csv(p)
    assert result.rows == 2
    assert result.errors == []

def test_invalid_dataset(tmp_path: pathlib.Path):
    p = tmp_path / "bad.csv"
    rows = [
        {"id": "1", "name": "Ana",  "age": "-1", "score": "1.0"},   # age negativo
        {"id": "1", "name": "   ",  "age": "x",  "score": "-2.0"},  # id duplicado, name vacío, age inválido, score negativo
        {"id": "y", "name": "M",    "age": "3",  "score": "z"},     # id inválido, score inválido
    ]
    _write_csv(p, rows)
    result = validate_csv(p)
    assert result.rows == 3
    # Debe haber varios errores
    assert any("age negativo" in e for e in result.errors)
    assert any("id duplicado" in e for e in result.errors)
    assert any("name vacío" in e for e in result.errors)
    assert any("age no es entero válido" in e for e in result.errors)
    assert any("id no es entero válido" in e for e in result.errors)
    assert any("score negativo" in e for e in result.errors) or any("score no es float válido" in e for e in result.errors)
