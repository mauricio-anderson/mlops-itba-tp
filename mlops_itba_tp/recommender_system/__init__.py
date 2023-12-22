""" """
from dagster import Definitions

from .assets import core_assets, recommender_assets

defs = Definitions(
    assets=[*core_assets, *recommender_assets],
)
