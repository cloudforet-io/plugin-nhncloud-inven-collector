import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.connector.block_storage.snapshot_connector import BlockStorageSnapshotsConnector
from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class BlockStorageSnapshotsManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Block Storage"
        self.cloud_service_type = "Snapshots"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/block_storage/snapshots.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/block_storage.png"
            },
            labels=["Management"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        block_connector = BlockStorageSnapshotsConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = block_connector.get_snapshots(secret_data, AVAILABLE_REGION)
            for resource in resources:
                reference = {
                    "resource_id": resource.get("id")
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
