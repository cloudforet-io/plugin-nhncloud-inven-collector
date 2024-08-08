import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.transit_hub.attachment_connector import AttachmentConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger('cloudforet')

class AttachmentManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Transit Hub"
        self.cloud_service_type = "Attachment"
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
                "spaceone:icon": f"{ASSET_URL}/transit_hub.png"
            },
            labels=["Networking"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        attachment_connector = AttachmentConnector()

        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            attachments = attachment_connector.list_attachments(secret_data.get("tenant_id"), secret_data.get("username"), secret_data.get("password"), AVAILABLE_REGION)
            for attachment in attachments:
                reference = {
                    "resource_id": attachment.get("id"),
                    "external_link": ""
                }

                cloud_service = make_cloud_service(
                    name=attachment["name"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=attachment,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service