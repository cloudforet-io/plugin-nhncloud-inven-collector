import logging
from spaceone.inventory.plugin.collector.lib import *

from src.plugin.conf.cloud_service_conf import AUTH_TYPE
from src.plugin.connector.instance.instance_type_connector import InstanceTypeConnector
from src.plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class InstanceTypeManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Instance"
        self.cloud_service_type = "Instance-Type"
        self.provider = "NHNCloud"
        self.metadata_path = "metadata/resource/instance/instance_type.yaml"

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
        instance_connector = InstanceTypeConnector()
        resources = instance_connector.get_types(secret_data)
        # {
        #     "flavors": [
        #         {
        #             "id": "0dc63e3d-3e92-4164-9bfe-447dd60a5b5c",
        #             "name": "g2.v100.c32m360",
        #             "links": [
        #                 {"href": "https://kr1-api-instance-infrastructure.nhncloudservice.com/v2.1/flavors/0dc63e3d-3e92-4164-9bfe-447dd60a5b5c",
        #                     "rel": "self"},
        #                 {"href": "https://kr1-api-instance-infrastructure.nhncloudservice.com/flavors/0dc63e3d-3e92-4164-9bfe-447dd60a5b5c",
        #                     "rel": "bookmark"}
        #             ]
        #         },
        #         {...}
        #     ]
        # }
        for resource in resources['flavors']:
            print(resource)
            reference = {
                "resource_id": resource.get("id"),
                "external_link": resource["links"][0]["href"]
            }
            cloud_service = make_cloud_service(
                name=resource["name"],
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
