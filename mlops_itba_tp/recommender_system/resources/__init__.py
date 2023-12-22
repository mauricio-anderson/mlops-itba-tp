""" """
# from dagster import EnvVar
from dagster_airbyte import AirbyteResource
from dagster_dbt import DbtCliResource

airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    username="airbyte",
    password="password",  # TODO: get password from EnvVar("AIRBYTE_PASSWORD")
)

PROJECT_DIR="/Users/mauricio.anderson/proyectos/mlops-itba-tp/dbt_project"  # TODO: replace with EnvVar("DBT_PROJECT_DIR")
dbt_resource = DbtCliResource(
    project_dir=PROJECT_DIR,
    target="dev",
)
