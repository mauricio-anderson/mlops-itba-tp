""" """
from dagster import Definitions

from .assets import recommender_assets, core_assets

# from .resources import airbyte_instance
# from dagster_airbyte import load_assets_from_airbyte_instance
# airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)


defs = Definitions(
    assets=[*core_assets, *recommender_assets],
)
