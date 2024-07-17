import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL
from plugin.connector.dns_plus.pool_connector import PoolConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger('cloudforet')

class PoolManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "DNS Plus"
        self.cloud_service_type = "Pool"
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
            }
        )
        return cloud_service_type

    def create_cloud_service(self, secret_data):
        pool_connector = PoolConnector()

        pools = pool_connector.list_pools(secret_data.get("app_key"))
        for pool in pools:
            reference = {
                "resource_id": pool.get("poolId"),
                "external_link": ""
            }

            cloud_service = make_cloud_service(
                name=pool["poolName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=pool,
                account=secret_data.get("project_id"),
                reference=reference
            )
            yield cloud_service
