""" """
from pathlib import Path

import pandas as pd
from dagster_dbt import DbtCliResource, dbt_assets
from dagster import Output, MetadataValue, AssetExecutionContext, asset

from mlops_itba_tp.utils.data import run_query

project_dir = Path(__file__).joinpath("..", "..", "..", "..", "..").resolve()
dbt_manifest_path = str(Path(project_dir)) + "/dbt_project/target/manifest.json"


@dbt_assets(manifest=dbt_manifest_path)
def rec_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@asset(
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
