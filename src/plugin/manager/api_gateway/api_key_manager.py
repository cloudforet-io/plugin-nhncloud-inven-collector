import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL, REGION
from plugin.connector.api_gateway.api_key_connector import APIKeyConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class APIKeyManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "API Gateway"
        self.cloud_service_type = "API Key"
        self.metadata_path = f"metadata/{self.cloud_service_group.replace(' ', '_').lower()}/{self.cloud_service_type.replace(' ', '_').lower()}.yaml"

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
        api_key_connector = APIKeyConnector()

        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            keys = api_key_connector.list_keys(secret_data.get("app_key"), AVAILABLE_REGION)
            for key in keys:
                reference = {
                    "resource_id": key.get("apiKeyId"),
                    "external_link": ""
                }

                cloud_service = make_cloud_service(
                    name=key["apiKeyName"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=key,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service

