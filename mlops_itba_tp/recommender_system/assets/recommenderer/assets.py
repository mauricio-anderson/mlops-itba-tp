""" """
from dagster import asset, Output, String, AssetIn, FreshnessPolicy, MetadataValue

@asset()
def hello() -> None:
    """ """
    print("hello world")
    return None
