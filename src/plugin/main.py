import logging
from typing import Generator
from spaceone.inventory.plugin.collector.lib.server import CollectorPluginServer

from plugin.manager.base import NHNCloudBaseManager

app = CollectorPluginServer()

_LOGGER = logging.getLogger("cloudforet")


@app.route("Collector.init")
def collector_init(params: dict) -> dict:
    return {"metadata": {"options_schema": {}}}

@app.route("Collector.verify")
def collector_verify(params: dict) -> None:
    # Verify connector using secret
    pass


def _check_secret_data(secret_data):
    pass


def _check_schema(schema):
    pass


@app.route("Collector.collect")
def collector_collect(params: dict) -> Generator[dict, None, None]:
    secret_data = params.get("secret_data", {})
    schema = params.get("schema", "")

    _check_secret_data(secret_data)
    _check_schema(schema)

    # Temporal code. This will be deleted when local testing using schema properties becomes possible.
    auth_type = NHNCloudBaseManager.get_auth_type_by_secret_data(secret_data)

    for manager in NHNCloudBaseManager.list_managers_by_schema(auth_type.value):
        yield from manager().collect_resources(secret_data)
