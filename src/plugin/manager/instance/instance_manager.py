import json
import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.block_storage.block_storage_connector import BlockStorageConnector
from plugin.connector.instance.instance_connector import InstanceConnector
from plugin.connector.security_group.security_group_connector import SGConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class InstanceManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Instance"
        self.cloud_service_type = "Instance"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/instance/instance.yaml"

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
            labels=["Compute", "Server"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        instance_connector = InstanceConnector()
        block_connector = BlockStorageConnector()
        sg_connector = SGConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = instance_connector.get_servers(secret_data, AVAILABLE_REGION)
            for resource in resources:
                volume_list = resource['os-extended-volumes:volumes_attached']
                volume_info_list = []
                for volume in volume_list:
                    volume_info = block_connector.get_volume_detail(secret_data, AVAILABLE_REGION, volume['id'])
                    volume_info_list.append(volume_info)
                resource['volumes'] = volume_info_list

                network_list = resource['addresses'].keys() # addresses 이름이 동적이기때문에 직접 커스텀
                network_info_list = []
                for network_name in network_list:
                    network_info_list.append(resource['addresses'][network_name])
                resource['networks'] = network_info_list

                self.make_security_group_response(AVAILABLE_REGION, resource, secret_data, sg_connector)

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
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service

    def make_security_group_response(self, AVAILABLE_REGION, resource, secret_data, sg_connector):
        sg_list = []
        security_group_list = resource['security_groups']

        for sg in security_group_list:
            sg_details_list = sg_connector.get_security_groups(secret_data, AVAILABLE_REGION, sg['name'])
            for sg_details in sg_details_list:
                security_group_name = sg_details['name']
                security_group_id = sg_details['id']

                # 각 security_group_rule에 security_group의 id와 name을 추가
                for rule in sg_details['security_group_rules']:
                    rule['group_id'] = security_group_id
                    rule['group_name'] = security_group_name

                sg_list.append(sg_details)
        resource['security_groups'] = sg_list
