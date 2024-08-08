import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL
from plugin.connector.dns_plus.health_check_connector import HealthCheckConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger('cloudforet')

class HealthCheckManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "DNS Plus"
        self.cloud_service_type = "Health Check"
        self.metadata_path = f"metadata/{self.cloud_service_group.replace(' ', '_').lower()}/{self.cloud_service_type.replace(' ', '_').lower()}.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=False,
            is_major=False,
            tags={
                "spaceone:icon": f"{ASSET_URL}/dns_plus.png"
            },
            labels=["Networking"]
        )
        return cloud_service_type

    def create_cloud_service(self, secret_data):
        health_check_connector = HealthCheckConnector()

        health_checks = health_check_connector.list_health_checks(secret_data.get("app_key"))

        for health_check in health_checks:
            reference = {
                "resource_id": health_check.get("healthCheckId"),
                "external_link": ""
            }

            health_check['requestHeaderList'] = list(map(str, health_check.get('requestHeaderList', [])))

            cloud_service = make_cloud_service(
                name=health_check["healthCheckName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=health_check,
                account=secret_data.get("project_id"),
                reference=reference
            )
            yield cloud_service
