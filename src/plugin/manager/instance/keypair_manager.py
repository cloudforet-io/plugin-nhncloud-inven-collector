import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.instance.keypair_connector import KeyPairConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class KeyPairManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Instance"
        self.cloud_service_type = "KeyPair"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/instance/keypair.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/instance.png"
            },
            labels=["Compute"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        keypair_connector = KeyPairConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = keypair_connector.get_keypair(secret_data, AVAILABLE_REGION)
            for resource in resources:
                detail = keypair_connector.get_keypair_detail(secret_data, resource['keypair']['name'], AVAILABLE_REGION)
                reference = {
                    "resource_id": resource.get("name")
                }
                cloud_service = make_cloud_service(
                    name=detail['name'],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=detail,
                    account=secret_data.get("username", None),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service
