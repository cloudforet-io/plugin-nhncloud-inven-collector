import json
import logging
from spaceone.inventory.plugin.collector.lib import *

from src.plugin.conf.cloud_service_conf import AUTH_TYPE
from src.plugin.connector.image.image_connector import ImageConnector
from src.plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class ImageManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Image"
        self.cloud_service_type = "Image"
        self.provider = "NHNCloud"
        self.metadata_path = "metadata/resource/image/image.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        image_connector = ImageConnector()
        resources = image_connector.get_image(secret_data)
        print(json.dumps(resources, indent=4))
        for resource in resources['images']:
            reference = {
                "resource_id": resource.get("id"),
            }
            cloud_service = make_cloud_service(
                name=resource['name'],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=resource,
                account=secret_data.get("username", None),
                reference=reference,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )
