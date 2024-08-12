import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL, REGION
from plugin.connector.nks.nks_connector import NKSConnector
from plugin.connector.nks.group_connector import NKSGroupConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class NKSGroupManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Container"
        self.cloud_service_type = "Node Group"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/nks/group.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/nks.png"
            },
            labels=["Container, Compute"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        group_connector = NKSGroupConnector()
        cluster_connector = NKSConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            for cluster in cluster_connector.get_cluster(secret_data, AVAILABLE_REGION):
                cluster_id = cluster['uuid']
                resources = group_connector.get_node_group(secret_data, cluster_id, AVAILABLE_REGION)
                for resource in resources:
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
                        account=secret_data.get("username", None),
                        reference=reference,
                    )
                    yield cloud_service
