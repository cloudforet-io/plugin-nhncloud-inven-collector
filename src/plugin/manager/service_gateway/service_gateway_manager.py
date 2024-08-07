import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.connector.service_gateway.service_gateway_connector import ServiceGatewayConnector
from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class ServiceGatewayManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Service Gateway"
        self.cloud_service_type = "Service Gateway"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/service_gateway/service_gateway.yaml"

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
            },
            labels=["Networking"]
        )
        return cloud_service_type

    def create_cloud_service(self, secret_data):
        gw_connector = ServiceGatewayConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = gw_connector.get_gateways(secret_data, AVAILABLE_REGION)
            for resource in resources:
                detail = gw_connector.get_detail(secret_data, resource['id'], AVAILABLE_REGION)
                reference = {
                    "resource_id": resource.get("id")
                }
                cloud_service = make_cloud_service(
                    name=resource['name'],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=detail,
                    account=secret_data.get("username", None),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service
