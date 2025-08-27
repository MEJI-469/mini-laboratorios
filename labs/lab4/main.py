# labs/lab4/main.py
"""
Lab 4 — Análisis Tabular con pandas y DuckDB
Ejecuta: python labs/lab4/main.py
Requisitos: pandas, duckdb, pyarrow
"""

from __future__ import annotations
import os
from pathlib import Path
import pandas as pd
import duckdb


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "ventas_demo.csv"
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def asegurar_dataset() -> None:
    """Crea un CSV pequeño si no existe."""
    if DATA_PATH.exists():
        return

    # Dataset de ejemplo (20 filas, con algunos nulos deliberados)
    df = pd.DataFrame({
        "id": range(1, 21),
        "fecha": pd.date_range("2024-01-01", periods=20, freq="D"),
        "categoria": ["A", "B", "C", "A", "B"] * 4,
        "producto": ["Prod1", "Prod2", "Prod3", "Prod4"] * 5,
        "precio": [10, 12, None, 11, 13] * 4,      # nulo deliberado
        "cantidad": [1, 2, 3, None, 2] * 4,        # nulo deliberado
        "cliente": ["  ana", "LUIS ", "marta", " Ana", "  luis"] * 4,
    })
    df.to_csv(DATA_PATH, index=False)
    print(f"[INFO] CSV de ejemplo creado en: {DATA_PATH}")


# ---------------------------
# Parte A — pandas
# ---------------------------
def parte_a_pandas():
    print("\n=== Parte A — pandas ===")

    df = pd.read_csv(DATA_PATH)
    print(f"[Exploración] Forma: {df.shape[0]} filas x {df.shape[1]} columnas")
    print("[Tipos]:")
    print(df.dtypes)
    print("\n[Nulos por columna]:")
    print(df.isna().sum())

    # Columna clave (ejemplo): 'id' y 'fecha'
    print("\n[Columna clave] id (entero) y fecha (temporal)")

    # Limpieza / derivadas
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    # Normalizamos texto (cliente) y categoría a MAYÚSCULAS
    df["cliente"] = df["cliente"].astype(str).str.strip().str.title()
    df["categoria"] = df["categoria"].astype(str).str.upper()

    # Gestionar nulos (decisión: precio nulos=0.0; cantidad nulos=1)
    df["precio"] = df["precio"].fillna(0.0)
    df["cantidad"] = df["cantidad"].fillna(1).astype(int)

    # Columna derivada: importe = precio * cantidad
    df["importe"] = df["precio"] * df["cantidad"]

    # Columna derivada temporal: mes (YYYY-MM)
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)

    print("\n[Preview limpio]:")
    print(df.head())

    # Filtro (ejemplo): filas con precio > 10
    filtrado = df.query("precio > 10")

    # Agrupación por mes y categoria con métricas
    resumen = (
        filtrado.groupby(["mes", "categoria"])
        .agg(
            total_importe=("importe", "sum"),
            unidades=("cantidad", "sum"),
            precio_promedio=("precio", "mean"),
        )
        .reset_index()
        .sort_values(["mes", "categoria"])
    )

    print("\n[Resumen pandas]:")
    print(resumen)

    # Exportes
    out_csv = OUT_DIR / "pandas_resumen.csv"
    out_parquet = OUT_DIR / "pandas_resumen.parquet"
    resumen.to_csv(out_csv, index=False)
    resumen.to_parquet(out_parquet, index=False)
    print(f"\n[Exportado] {out_csv}")
    print(f"[Exportado] {out_parquet}")


# ---------------------------
# Parte B — DuckDB
# ---------------------------
def parte_b_duckdb():
    print("\n=== Parte B — DuckDB (SQL embebido) ===")

    # B.1: primer query sobre el archivo (sin pasar por pandas)
    cnt = duckdb.query(f"SELECT COUNT(*) AS filas FROM read_csv_auto('{DATA_PATH.as_posix()}', HEADER=True);").to_df()
    print("[Conteo directo CSV con DuckDB]:")
    print(cnt)

    # SELECT que replica el análisis de pandas:
    # - Limpieza equivalente (precio nulo->0, cantidad nula->1, cliente trim/title, categoria upper)
    # - Derivadas: importe, mes
    # - Filtro: precio > 10
    select_sql = f"""
    WITH base AS (
        SELECT 
            CAST(id AS BIGINT) AS id,
            CAST(fecha AS DATE) AS fecha,
            UPPER(CAST(categoria AS VARCHAR)) AS categoria,
            CAST(producto AS VARCHAR) AS producto,
            COALESCE(CAST(precio AS DOUBLE), 0.0) AS precio,
            COALESCE(CAST(cantidad AS BIGINT), 1) AS cantidad,
            TRIM(CAST(cliente AS VARCHAR)) AS cliente_raw
        FROM read_csv_auto('{DATA_PATH.as_posix()}', HEADER=True)
    ),
    limpio AS (
        SELECT
            id,
            fecha,
            categoria,
            producto,
            precio,
            cantidad,
            UPPER(SUBSTR(TRIM(cliente_raw), 1, 1)) || LOWER(SUBSTR(TRIM(cliente_raw), 2)) AS cliente,
            date_trunc('month', fecha)  AS mes_date,
            precio * cantidad           AS importe
        FROM base
    ),
    filtrado AS (
        SELECT *
        FROM limpio
        WHERE precio > 10
    )
    SELECT
        strftime(mes_date, '%Y-%m') AS mes,
        categoria,
        SUM(importe)       AS total_importe,
        SUM(cantidad)      AS unidades,
        AVG(precio)        AS precio_promedio
    FROM filtrado
    GROUP BY 1, 2
    ORDER BY 1, 2
    """

    resumen_sql_df = duckdb.query(select_sql).to_df()
    print("\n[Resumen DuckDB]:")
    print(resumen_sql_df)

    # Exportes nativos desde DuckDB
    duck_csv = OUT_DIR / "duckdb_resumen.csv"
    duck_parquet = OUT_DIR / "duckdb_resumen.parquet"

    duckdb.query(f"COPY ({select_sql}) TO '{duck_csv.as_posix()}' (HEADER, DELIMITER ',');")
    duckdb.query(f"COPY ({select_sql}) TO '{duck_parquet.as_posix()}' (FORMAT PARQUET);")

    print(f"\n[Exportado] {duck_csv}")
    print(f"[Exportado] {duck_parquet}")


def main():
    asegurar_dataset()
    parte_a_pandas()
    parte_b_duckdb()
    print("\n✅ Lab 4 completado. Archivos en:", OUT_DIR)


if __name__ == "__main__":
    main()
