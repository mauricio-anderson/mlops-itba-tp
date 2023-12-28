""" """
from dagster import job
from dagster_airbyte import airbyte_sync_op

from mlops_itba_tp.recommender_system.resources import airbyte_instance

sync_movies = airbyte_sync_op.configured(
    {"connection_id": "5db5fc4f-883c-47a2-9bf0-aaacdfb66423"}, name="sync_movies"
)

sync_users = airbyte_sync_op.configured(
    {"connection_id": "63c24a73-c9a6-43cb-aba7-891cbdeaa504"}, name="sync_users"
)

sync_scores = airbyte_sync_op.configured(
    {"connection_id": "eda835ef-32ff-408a-aa8c-47a92549b2c9"}, name="sync_scores"
)


@job(name="airbyte_sync_job", resource_defs={"airbyte": airbyte_instance})
def airbyte_job():
    sync_movies()
    sync_users()
    sync_scores()
