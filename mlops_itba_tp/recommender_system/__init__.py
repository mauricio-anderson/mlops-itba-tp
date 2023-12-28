""" """
from dagster import Definitions, ScheduleDefinition, define_asset_job, AssetSelection

from .resources import dbt_resource
from .assets.core.jobs import airbyte_job
from .assets import core_assets, recommender_assets

training_config = {
    "keras_dot_product_model": {
        "config": {
            "batch_size": 128,
            "epochs": 10,
            "learning_rate": 1e-3,
            "embeddings_dim": 5,
        }
    }
}

get_data_job = define_asset_job(
    name="get_data",
    # selection=["movies", "users", "scores", "table_to_model", "training_data"],
    selection=AssetSelection.groups('core'),
    config={},
)

train_model_job = define_asset_job(
    name="train_model",
    selection=AssetSelection.groups('recommender'),
    config={'ops': {**training_config}},
)

airflow_sync_schedule = ScheduleDefinition(
    job=airbyte_job,
    cron_schedule="0 * * * *",  # every hour
)

defs = Definitions(
    assets=[*core_assets, *recommender_assets],
    jobs=[
        airbyte_job,
        get_data_job,
        train_model_job,
    ],
    schedules=[airflow_sync_schedule],
    resources={
        "dbt": dbt_resource,
    },
)
