import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from ..connector.resource_connector import ResourceConnector

_LOGGER = logging.getLogger("cloudforet")


class ResourceManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Change the following variables to match the actual resource group and type
        self.cloud_service_group = "ResourceGroup-A"
        self.cloud_service_type = "Resource-A"
        self.provider = "example"
        self.metadata_path = "metadata/resource/resource.yaml"

    def collect_resources(self, options, secret_data, schema):
        try:
            yield from self._collect_cloud_service_type(options, secret_data, schema)
            yield from self._collect_cloud_service(options, secret_data, schema)
        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def _collect_cloud_service_type(self, options, secret_data, schema):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
        )

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "reference.resource_id", "account", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def _collect_cloud_service(self, options, secret_data, schema):
        resource_connector = ResourceConnector()
        resources = resource_connector.list_servers()
        for resource in resources["servers_info"]:
            reference = {
                    "resource_id": resource.get("id"),
                    "external_link": "https://github.com/cloudforet-io/plugin-example-inven-collector"
                    }
            cloud_service = make_cloud_service(
                name=resource["name"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=resource,
                account=secret_data.get("account_id",None),
                reference=reference,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )
