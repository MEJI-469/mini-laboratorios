# Lab 4 — pandas vs DuckDB (resumen rápido)

## ¿Qué hicimos?
- **pandas**: leímos CSV, exploramos tipos y nulos, normalizamos texto/fechas, creamos derivadas (`importe`, `mes`), filtramos (`precio > 10`), agrupamos por `mes` y `categoria`, y exportamos a CSV/Parquet.
- **DuckDB**: ejecutamos SQL directamente **sobre el CSV** (sin cargar antes en pandas), replicando limpieza/derivadas/filtros/agrupación y exportando resultados con `COPY`.

## ¿Cuándo conviene cada enfoque?
- **pandas**: exploración interactiva, transformaciones complejas fila a fila, integración con ecosistema PyData (NumPy, scikit-learn). Excelente para análisis en notebooks y prototipos.
- **DuckDB (SQL embebido)**: consultas SQL expresivas, lectura directa de archivos (CSV/Parquet), agrupaciones grandes, compatibilidad con pipelines SQL. Muy útil cuando ya piensas en SQL o quieres performance en joins/aggregations.

## Salidas
- `labs/lab4/output/pandas_resumen.(csv|parquet)`
- `labs/lab4/output/duckdb_resumen.(csv|parquet)`
