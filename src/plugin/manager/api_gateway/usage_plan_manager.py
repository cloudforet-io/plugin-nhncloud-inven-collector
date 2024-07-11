import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.api_gateway.usage_plan_connector import UsagePlanConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class UsagePlanManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "API Gateway"
        self.cloud_service_type = "Usage Plan"
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
        usage_plan_connector = UsagePlanConnector()

        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            usage_plans = usage_plan_connector.list_usage_plans(secret_data.get("app_key"), AVAILABLE_REGION)
            for usage_plan in usage_plans:
                reference = {
                    "resource_id": usage_plan.get("usagePlanId"),
                    "external_link": ""
                }

                cloud_service = make_cloud_service(
                    name=usage_plan["usagePlanName"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=usage_plan,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service

