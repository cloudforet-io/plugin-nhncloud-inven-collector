import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL
from plugin.connector.dns_plus.gslb_connector import GSLBConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class GSLBManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "DNS Plus"
        self.cloud_service_type = "GSLB"
        self.metadata_path = f"metadata/{self.cloud_service_group.replace(' ', '_').lower()}/{self.cloud_service_type.replace(' ', '_').lower()}.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=False,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/dns_plus.png"
            }
        )
        return cloud_service_type

    def create_cloud_service(self, secret_data):
        gslb_connector = GSLBConnector()

        gslbs = gslb_connector.list_gslbs(secret_data.get("app_key"))

        for gslb in gslbs:
            reference = {
                "resource_id": gslb.get("gslbId"),
                "external_link": ""
            }

            for pool in gslb.get("connectedPoolList", []):
                pool["pool"]["endpointLength"] = len(pool["pool"].get("endpointList", []))

            cloud_service = make_cloud_service(
                name=gslb["gslbName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=gslb,
                account=secret_data.get("project_id"),
                reference=reference,
            )
            yield cloud_service