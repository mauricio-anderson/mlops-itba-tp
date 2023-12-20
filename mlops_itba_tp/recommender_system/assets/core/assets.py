""" """
from dagster import asset, Output, String, AssetIn, FreshnessPolicy, MetadataValue
from mlops_itba_tp.utils.data import run_query
import pandas as pd

@asset()
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
