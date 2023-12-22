""" """
import pandas as pd
from dagster_airbyte import build_airbyte_assets
from dagster import Output, MetadataValue, asset, with_resources

from mlops_itba_tp.utils.data import run_query
from mlops_itba_tp.recommender_system.resources import airbyte_instance


movie_assets = with_resources(
    build_airbyte_assets(
        connection_id="5db5fc4f-883c-47a2-9bf0-aaacdfb66423",
        destination_tables=["movies"],
    ),
    {"airbyte": airbyte_instance},
)

user_assets = with_resources(
    build_airbyte_assets(
        connection_id="63c24a73-c9a6-43cb-aba7-891cbdeaa504",
        destination_tables=["users"],
    ),
    {"airbyte": airbyte_instance},
)

score_assets = with_resources(
    build_airbyte_assets(
        connection_id="eda835ef-32ff-408a-aa8c-47a92549b2c9",
        destination_tables=["scores"],
    ),
    {"airbyte": airbyte_instance},
)


@asset(deps=[*movie_assets, *user_assets, *score_assets])
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
