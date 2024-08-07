import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.transit_hub.shared_multicast_domain_connector import SharedMulticastDomainConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class SharedMulticastDomainManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Transit Hub"
        self.cloud_service_type = "Shared Multicast Domain"
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
        shared_multicast_domain_connector = SharedMulticastDomainConnector()

        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            shared_multicast_domains = shared_multicast_domain_connector.list_shared_multicast_domains(secret_data.get("tenant_id"), secret_data.get("username"), secret_data.get("password"), AVAILABLE_REGION)
            for shared_multicast_domain in shared_multicast_domains:
                reference = {
                    "resource_id": shared_multicast_domain.get("domain_id"),
                    "external_link": ""
                }

                cloud_service = make_cloud_service(
                    name=shared_multicast_domain["domain_name"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=shared_multicast_domain,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service