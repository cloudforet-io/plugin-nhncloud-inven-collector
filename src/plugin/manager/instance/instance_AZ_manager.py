import logging
from spaceone.inventory.plugin.collector.lib import *

from src.plugin.conf.cloud_service_conf import AUTH_TYPE
from src.plugin.connector.instance.instance_AZ_connector import InstanceAZConnector
from src.plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class InstanceAZManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Change the following variables to match the actual resource group and type
        self.cloud_service_group = "Instance"
        self.cloud_service_type = "Instance-AZ"
        self.provider = "NHNCloud"
        self.metadata_path = "metadata/resource/instance/instance_AZ_resource.yaml"

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
        resource_connector = InstanceAZConnector()
        resources = resource_connector.get_availability_zone(secret_data)
        # {
        #     "availabilityZoneInfo": [
        #         {
        #             "zoneState": {
        #                 "available": true
        #             },
        #             "hosts": null,
        #             "zoneName": "kr-pub-b"
        #         },
        #         { ... }
        #     ]
        # }
        for resource in resources["availabilityZoneInfo"]:
            reference = {
                "resource_id": resource.get("zoneName")
            }
            cloud_service = make_cloud_service(
                name=resource["zoneName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=resource,
                account=secret_data.get("username", None),
                reference=reference,
            )
            print(cloud_service)
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )
