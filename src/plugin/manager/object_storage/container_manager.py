import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.object_storage.container_connector import ContainerConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class ContainerManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.OBJECT_STORAGE_TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1, REGION.US1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Object Storage"
        self.cloud_service_type = "Container"
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
                "spaceone:icon": f"{ASSET_URL}/object_storage.png"
            },
            labels=["Storage"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        container_connector = ContainerConnector()

        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            containers = container_connector.list_containers(secret_data.get("object_storage_tenant_id"), secret_data.get("username"), secret_data.get("object_storage_password"), secret_data.get("storage_account"), AVAILABLE_REGION)
            for container in containers:
                reference = {
                    "resource_id": container.get("name"),
                    "external_link": ""
                }

                cloud_service = make_cloud_service(
                    name=container["name"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=container,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name,
                    instance_size=container.get("bytes", 0)
                )
                yield cloud_service