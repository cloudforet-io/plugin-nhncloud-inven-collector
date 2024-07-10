import json
import logging
from spaceone.inventory.plugin.collector.lib import *

from src.plugin.conf.cloud_service_conf import AUTH_TYPE
from src.plugin.connector.nks.nks_connector import NKSConnector
from src.plugin.connector.nks.nks_group_connector import NKSGroupConnector
from src.plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class NKSGroupManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Container"
        self.cloud_service_type = "Node Group"
        self.provider = "NHNCloud"
        self.metadata_path = "metadata/resource/nks/nks_group.yaml"

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
        group_connector = NKSGroupConnector()
        cluster_connector = NKSConnector()
        for cluster in cluster_connector.get_cluster(secret_data)['clusters']:
            cluster_id = cluster['uuid']
            resources = group_connector.get_node_group(cluster_id, secret_data)

            for resource in resources['nodegroups']:
                detail = group_connector.get_node_group_detail(cluster_id, resource['uuid'], secret_data)
                reference = {
                    "resource_id": resource.get("uuid")
                }
                cloud_service = make_cloud_service(
                    name=resource['name'],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=detail,
                    tags=detail['labels'],
                    account=secret_data.get("username", None),
                    reference=reference,
                )
                yield make_response(
                    cloud_service=cloud_service,
                    match_keys=[["name", "reference.resource_id", "account", "provider"]],
                )
