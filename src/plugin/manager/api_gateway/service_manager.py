import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL, REGION
from plugin.connector.api_gateway.service_connector import APIGatewayServiceConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class APIGatewayServiceManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "API Gateway"
        self.cloud_service_type = "Service"
        self.metadata_path = f"metadata/{self.cloud_service_group.replace(' ', '_').lower()}/{self.cloud_service_type.lower()}.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/api_gateway.png"
            }
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        service_connector = APIGatewayServiceConnector()

        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            services = service_connector.list_services(secret_data.get("app_key"), AVAILABLE_REGION)
            for service in services:
                reference = {
                    "resource_id": service.get("apigwServiceId"),
                    "external_link": ""
                }
                resources = service_connector.list_resources_by_service_id(secret_data.get("app_key"), service.get("apigwServiceId"), AVAILABLE_REGION)
                stages = service_connector.list_stages_by_service_id(secret_data.get("app_key"), service.get("apigwServiceId"), AVAILABLE_REGION)

                service.update({
                    "resources": resources,
                    "stages": stages
                })

                cloud_service = make_cloud_service(
                    name=service["apigwServiceName"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=service,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service

