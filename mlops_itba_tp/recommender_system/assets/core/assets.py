""" """
import pandas as pd
from dagster_dbt import DbtCliResource, dbt_assets
from dagster import Output, AssetIn, MetadataValue, AssetExecutionContext, asset

from mlops_itba_tp.utils.data import run_query

dbt_manifest_path = "/Users/mauricio.anderson/proyectos/mlops-itba-tp/dbt_project/target/manifest.json"  # TODO: replace for relative path


@dbt_assets(manifest=dbt_manifest_path)
def rec_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@asset(
    # ins={"table_to_model": AssetIn()},
    deps=["table_to_model"],
    compute_kind="python",
)
def training_data() -> Output[pd.DataFrame]:
    """ """
    query = """
        SELECT * FROM "processed_data"."table_to_model"
        """
    data = run_query(query)
    return Output(
        data,
        metadata={
            "Total rows": len(data),
            "preview": MetadataValue.md(data.head().to_markdown()),
        },
    )
