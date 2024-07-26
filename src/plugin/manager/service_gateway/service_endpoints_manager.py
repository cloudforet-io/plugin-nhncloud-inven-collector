import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.connector.service_gateway.service_endpoints_connector import ServiceEndpointsConnector
from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class ServiceEndpointsManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Service Gateway"
        self.cloud_service_type = "Service Endpoints"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/service_gateway/service_endpoints.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/service_gateway.png"
            }
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        endpoints_connector = ServiceEndpointsConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = endpoints_connector.get_endpoints(secret_data, AVAILABLE_REGION)
            for resource in resources:
                reference = {
                    "resource_id": resource.get("id")
                }
                cloud_service = make_cloud_service(
                    name=resource['name'],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=resource,
                    account=secret_data.get("username", None),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service
