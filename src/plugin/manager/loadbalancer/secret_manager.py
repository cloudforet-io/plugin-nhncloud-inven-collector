import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.loadbalancer.secret_connector import LoadBalancerSecretConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class LoadBalancerSecretManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "LoadBalancer"
        self.cloud_service_type = "Secrets"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/loadbalancer/secrets.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/load_balancer.png"
            },
            labels=["Networking", "Security"]
        )

        return cloud_service_type

    #TODO 페이징 처리!!!!!
    def create_cloud_service(self, secret_data):
        secrets_connector = LoadBalancerSecretConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = secrets_connector.get_secrets(secret_data, AVAILABLE_REGION)
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
