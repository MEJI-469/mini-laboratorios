from __future__ import annotations
import os
import io as pyio
import requests
import pandas as pd
from dagster import asset, asset_check, AssetCheckResult

# =========================
# Config
# =========================
OWID_URL = os.getenv(
    "OWID_URL",
    "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv",
)
OWID_LOCAL_PATH = os.getenv("OWID_LOCAL_PATH", "")
COMPARISON_COUNTRY = os.getenv("COMPARISON_COUNTRY", "Peru")
ALLOW_NEG = os.getenv("ALLOW_NEGATIVE_NEW_CASES", "false").lower() == "true"
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "final_project/output")

# =========================
# Helpers
# =========================
def _loc_col(df: pd.DataFrame) -> str:
    """Devuelve el nombre de la columna de país según el dataset:
    'location' (owid-covid-data) o 'country' (compact.csv)."""
    if "location" in df.columns:
        return "location"
    if "country" in df.columns:
        return "country"
    raise KeyError("No se encontró columna de país: 'location' o 'country'.")

def _scope_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra solo Ecuador + país comparativo (para checks)."""
    loc = _loc_col(df)
    return df[df[loc].isin(["Ecuador", COMPARISON_COUNTRY])].copy()

def procesar_base(df: pd.DataFrame, pais_a: str, pais_b: str) -> pd.DataFrame:
    df = df.copy()
    # Normaliza fecha a tz-naive
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True).dt.tz_convert(None)
    # Coerción numérica
    for col in ["new_cases", "people_vaccinated", "population"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # nulos críticos y duplicados clave
    loc = _loc_col(df)
    df = df.dropna(subset=["date", "new_cases", "people_vaccinated"])
    df = df.drop_duplicates(subset=[loc, "date"])
    # filtro de países y columnas esenciales
    df = df[df[loc].isin([pais_a, pais_b])]
    cols = [loc, "date", "new_cases", "people_vaccinated", "population"]
    df = df[cols].sort_values([loc, "date"]).reset_index(drop=True)
    # homogeneizamos a 'location' para el resto del pipeline
    return df.rename(columns={loc: "location"})

def compute_incidencia_7d(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values(["location", "date"])
    df["incidencia_diaria"] = (df["new_cases"] / df["population"]) * 100000
    df["incidencia_7d"] = (
        df.groupby("location")["incidencia_diaria"].transform(lambda s: s.rolling(7, min_periods=1).mean())
    )
    return df[["date", "location", "incidencia_7d"]].rename(columns={"date": "fecha", "location": "pais"})

def compute_factor_crec_7d(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values(["location", "date"])
    df["casos_semana"] = (
        df.groupby("location")["new_cases"].transform(lambda s: s.rolling(7, min_periods=7).sum())
    )
    df["casos_semana_prev"] = (
        df.groupby("location")["new_cases"].transform(lambda s: s.shift(7).rolling(7, min_periods=7).sum())
    )
    df["factor_crec_7d"] = df["casos_semana"] / df["casos_semana_prev"]
    out = df[["date", "location", "casos_semana", "factor_crec_7d"]].dropna()
    return out.rename(columns={"date": "semana_fin", "location": "pais"})

# =========================
# Assets
# =========================
@asset(description="Descarga el CSV de OWID (o lee de OWID_LOCAL_PATH) y devuelve un DataFrame crudo.")
def leer_datos(context) -> pd.DataFrame:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if OWID_LOCAL_PATH and os.path.exists(OWID_LOCAL_PATH):
        context.log.info(f"Leyendo CSV local: {OWID_LOCAL_PATH}")
        df = pd.read_csv(OWID_LOCAL_PATH)
    else:
        context.log.info(f"Descargando CSV desde: {OWID_URL}")
        resp = requests.get(OWID_URL, timeout=60)
        resp.raise_for_status()
        df = pd.read_csv(pyio.BytesIO(resp.content))
    context.log.info(f"Leídos {len(df):,} registros y {len(df.columns)} columnas.")
    return df

@asset(description="Perfilado básico y exporte a final_project/output/tabla_perfilado.csv")
def tabla_perfilado(context, leer_datos: pd.DataFrame) -> pd.DataFrame:
    df = leer_datos.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True).dt.tz_convert(None)
    new_cases = pd.to_numeric(df["new_cases"], errors="coerce")
    people_vacc = pd.to_numeric(df["people_vaccinated"], errors="coerce")
    perfil = pd.DataFrame([
        {"metric": "filas", "valor": len(df)},
        {"metric": "columnas", "valor": len(df.columns)},
        {"metric": "new_cases_min", "valor": float(new_cases.min(skipna=True))},
        {"metric": "new_cases_max", "valor": float(new_cases.max(skipna=True))},
        {"metric": "pct_null_new_cases", "valor": float(new_cases.isna().mean() * 100)},
        {"metric": "pct_null_people_vaccinated", "valor": float(people_vacc.isna().mean() * 100)},
        {"metric": "fecha_min", "valor": str(df["date"].min())},
        {"metric": "fecha_max", "valor": str(df["date"].max())},
    ])
    out_csv = os.path.join(OUTPUT_DIR, "tabla_perfilado.csv")
    perfil.to_csv(out_csv, index=False)
    context.log.info(f"Perfilado exportado: {out_csv}")
    return perfil

@asset(description="Limpia nulos/duplicados, filtra Ecuador + país comparativo y deja columnas esenciales.")
def datos_procesados(context, leer_datos: pd.DataFrame) -> pd.DataFrame:
    df = procesar_base(leer_datos, "Ecuador", COMPARISON_COUNTRY)
    context.log.info(f"Procesado: {len(df):,} filas. Países: Ecuador y {COMPARISON_COUNTRY}")
    return df

@asset(description="Incidencia acumulada a 7 días por 100k habitantes.")
def metrica_incidencia_7d(context, datos_procesados: pd.DataFrame) -> pd.DataFrame:
    out = compute_incidencia_7d(datos_procesados)
    context.log.info(f"Incidencia 7d -> {len(out):,} filas.")
    return out

@asset(description="Factor de crecimiento semanal (últimos 7 días / semana previa).")
def metrica_factor_crec_7d(context, datos_procesados: pd.DataFrame) -> pd.DataFrame:
    out = compute_factor_crec_7d(datos_procesados)
    context.log.info(f"Factor crecimiento 7d -> {len(out):,} filas.")
    return out

@asset(description="Exporta resultados finales a un Excel multipestaña.")
def reporte_excel_covid(
    context,
    datos_procesados: pd.DataFrame,
    metrica_incidencia_7d: pd.DataFrame,
    metrica_factor_crec_7d: pd.DataFrame,
) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_xlsx = os.path.join(OUTPUT_DIR, "reporte_covid.xlsx")
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        datos_procesados.to_excel(writer, sheet_name="datos_procesados", index=False)
        metrica_incidencia_7d.to_excel(writer, sheet_name="incidencia_7d", index=False)
        metrica_factor_crec_7d.to_excel(writer, sheet_name="factor_crec_7d", index=False)
    context.log.info(f"Reporte exportado: {out_xlsx}")
    return out_xlsx

# =========================
# Asset Checks (ajustados)
# =========================
@asset_check(asset="leer_datos", description="La fecha máxima (con datos) no debe estar en el futuro.")
def check_no_future_dates(context, leer_datos: pd.DataFrame) -> AssetCheckResult:
    d = _scope_rows(leer_datos)
    d["date"] = pd.to_datetime(d["date"], errors="coerce", utc=True).dt.tz_convert(None)
    # Sólo filas con datos reales
    has_data = pd.to_numeric(d.get("new_cases"), errors="coerce").notna()
    d = d.loc[has_data]
    max_date = d["date"].max()
    today = pd.Timestamp.utcnow().tz_localize(None).normalize()
    n_future = int((d["date"] > today).sum())
    passed = pd.isna(max_date) or (max_date <= today)
    return AssetCheckResult(
        passed=passed,
        metadata={
            "max_date": str(max_date),
            "today": str(today),
            "rows_checked": len(d),
            "future_rows": n_future,
        },
    )

@asset_check(asset="leer_datos", description="Sin nulos en país/date/población para los países objetivo.")
def check_key_columns_not_null(context, leer_datos: pd.DataFrame) -> AssetCheckResult:
    loc = _loc_col(leer_datos)
    d = _scope_rows(leer_datos)
    req_cols = [loc, "date", "population"]
    subset_nulls = {c: int(d[c].isna().sum()) for c in req_cols if c in d.columns}
    global_pop_nulls = int(pd.to_numeric(leer_datos.get("population"), errors="coerce").isna().sum())
    passed = all(subset_nulls.get(c, 1) == 0 for c in req_cols)
    return AssetCheckResult(
        passed=passed,
        metadata={
            "subset_nulls": subset_nulls,
            "global_population_nulls": global_pop_nulls,
            "countries": f"Ecuador & {COMPARISON_COUNTRY}",
            "subset_rows": len(d),
        },
    )

@asset_check(asset="leer_datos", description="(país, date) debe ser único.")
def check_unique_location_date(context, leer_datos: pd.DataFrame) -> AssetCheckResult:
    loc = _loc_col(leer_datos)
    if not {loc, "date"}.issubset(leer_datos.columns):
        return AssetCheckResult(passed=False, metadata={"error": f"Faltan columnas {loc} o date"})
    dupes = int(leer_datos.duplicated(subset=[loc, "date"]).sum())
    return AssetCheckResult(passed=(dupes == 0), metadata={"duplicados": dupes})

@asset_check(asset="leer_datos", description="Población > 0.")
def check_population_positive(context, leer_datos: pd.DataFrame) -> AssetCheckResult:
    pop = pd.to_numeric(leer_datos.get("population"), errors="coerce")
    non_pos = int((pop <= 0).sum()) if pop is not None else -1
    passed = (non_pos == 0) if pop is not None else False
    return AssetCheckResult(passed=passed, metadata={"poblacion_no_positiva": non_pos})

@asset_check(asset="leer_datos", description="Política de negativos en new_cases.")
def check_new_cases_policy(context, leer_datos: pd.DataFrame) -> AssetCheckResult:
    new_cases = pd.to_numeric(leer_datos.get("new_cases"), errors="coerce")
    neg_count = int((new_cases < 0).sum()) if new_cases is not None else -1
    if ALLOW_NEG:
        passed = True
        note = "Negativos permitidos (ALLOW_NEGATIVE_NEW_CASES=true)."
    else:
        passed = (neg_count == 0)
        note = "Negativos NO permitidos. Ajusta ALLOW_NEGATIVE_NEW_CASES si corresponde."
    return AssetCheckResult(passed=passed, metadata={"negativos": neg_count, "nota": note})

@asset_check(asset="metrica_incidencia_7d", description="Rango razonable: 0 ≤ incidencia_7d ≤ 2000.")
def check_incidencia_7d_rango(context, metrica_incidencia_7d: pd.DataFrame) -> AssetCheckResult:
    vals = pd.to_numeric(metrica_incidencia_7d["incidencia_7d"], errors="coerce")
    outliers = int(((vals < 0) | (vals > 2000)).sum())
    return AssetCheckResult(passed=(outliers == 0), metadata={"fuera_de_rango": outliers})
