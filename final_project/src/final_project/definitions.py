from dagster import Definitions, load_assets_from_modules
from final_project import assets as assets_module

defs = Definitions(
    assets=load_assets_from_modules([assets_module]),
    asset_checks=[
        assets_module.check_no_future_dates,
        assets_module.check_key_columns_not_null,
        assets_module.check_unique_location_date,
        assets_module.check_population_positive,
        assets_module.check_new_cases_policy,
        assets_module.check_incidencia_7d_rango,
    ],
)
