""" """
from dagster import Definitions, ScheduleDefinition, define_asset_job

from .resources import dbt_resource
from .assets import core_assets, recommender_assets
from .assets.core.jobs import airbyte_job

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

job_data_config = {}

get_data_job = define_asset_job(
    name="get_data",
    selection=["movies", "users", "scores", "training_data"],
    config=job_data_config,
)

get_data_schedule = ScheduleDefinition(
    job=airbyte_job,
    cron_schedule="0 * * * *",  # every hour
)

defs = Definitions(
    assets=[*core_assets, *recommender_assets],
    jobs=[airbyte_job, get_data_job],
    # schedules=[get_data_schedule,],
    resources={
        "dbt": dbt_resource,
    },
)
