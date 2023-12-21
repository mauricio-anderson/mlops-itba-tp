""" """
from dagster import EnvVar
from dagster_airbyte import AirbyteResource

airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    username="airbyte",
    password="password",  # TODO: get password from EnvVar("AIRBYTE_PASSWORD")
)
