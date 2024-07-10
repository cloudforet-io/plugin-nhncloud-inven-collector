import json
import logging
from spaceone.inventory.plugin.collector.lib import *

from src.plugin.conf.cloud_service_conf import AUTH_TYPE
from src.plugin.connector.instance.instance_connector import InstanceConnector
from src.plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class InstanceManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Instance"
        self.cloud_service_type = "Instance"
        self.provider = "NHNCloud"
        self.metadata_path = "metadata/resource/instance/instance.yaml"

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
        instance_connector = InstanceConnector()
        resources = instance_connector.get_servers(secret_data)
        print(json.dumps(resources, indent=4))
        for resource in resources['servers']:
            # volume_list = resource['os-extended-volumes:volumes_attached']
            # for volume_id in volume_list:
            #     volume = instance_connector.get_volume(resource['id'], resource[volume_id], secret_data)
            #     print(volume)
            reference = {
                "resource_id": resource.get("id"),
                "external_link": resource['links'][0]['href']
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
