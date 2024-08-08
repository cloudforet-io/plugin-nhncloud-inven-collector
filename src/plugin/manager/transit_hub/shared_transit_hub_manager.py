import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.transit_hub.shared_transit_hub_connector import SharedTransitHubConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class SharedTransitHubManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Transit Hub"
        self.cloud_service_type = "Shared Transit Hub"
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
                "spaceone:icon": f"{ASSET_URL}/transit_hub.png"
            },
            labels=["Networking"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        shared_transit_hub_connector = SharedTransitHubConnector()

        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            shared_transit_hubs = shared_transit_hub_connector.list_shared_transit_hubs(secret_data.get("tenant_id"), secret_data.get("username"), secret_data.get("password"), AVAILABLE_REGION)
            for shared_transit_hub in shared_transit_hubs:
                reference = {
                    "resource_id": shared_transit_hub.get("transithub_id"),
                    "external_link": ""
                }

                cloud_service = make_cloud_service(
                    name=shared_transit_hub["transithub_name"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=shared_transit_hub,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service