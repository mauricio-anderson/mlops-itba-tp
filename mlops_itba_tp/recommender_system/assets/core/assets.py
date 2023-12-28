""" """
import pandas as pd
from dagster_dbt import DbtCliResource, dbt_assets
from dagster import Output, MetadataValue, AssetExecutionContext, asset

dbt_manifest_path = "/Users/mauricio.anderson/proyectos/mlops-itba-tp/dbt_project/target/manifest.json"  # TODO: replace for relative path


@dbt_assets(manifest=dbt_manifest_path)
def rec_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@asset(compute_kind="python")
def training_data(table_to_model: pd.DataFrame) -> Output[pd.DataFrame]:
    """ """
    data = table_to_model
    return Output(
        data,
        metadata={
            "Total rows": len(data),
            "preview": MetadataValue.md(data.head().to_markdown()),
        },
    )
