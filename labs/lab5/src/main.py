from __future__ import annotations
from pathlib import Path
import csv

from textutils import normalize_spaces, word_count, is_palindrome
from csv_validation import validate_csv

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "sample.csv"

def ensure_sample_csv() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        return
    rows = [
        {"id": "1", "name": "Ana",   "age": "21", "score": "9.5"},
        {"id": "2", "name": "Luis",  "age": "19", "score": "7.0"},
        {"id": "3", "name": "Marta", "age": "22", "score": "10.0"},
    ]
    with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "age", "score"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[INFO] CSV de ejemplo creado en: {DATA_FILE}")

def demo_textutils() -> None:
    print("=== Parte A — textutils ===")
    s = "  Hola   mundo   de  pruebas  "
    print("normalize_spaces:", normalize_spaces(s))
    print("word_count:", word_count(s))
    print("is_palindrome('Anita lava la tina'):", is_palindrome("Anita lava la tina"))

def demo_csv_validation() -> None:
    print("\n=== Parte B — CSV validation ===")
    result = validate_csv(DATA_FILE)
    print("Filas leídas:", result.rows)
    if result.errors:
        print("[ERRORES]")
        for e in result.errors:
            print("-", e)
    else:
        print("Validación OK (sin errores).")

def main() -> None:
    ensure_sample_csv()
    demo_textutils()
    demo_csv_validation()
    print("\n✅ Lab 5 ejecutado correctamente desde main.py")

if __name__ == "__main__":
    main()
