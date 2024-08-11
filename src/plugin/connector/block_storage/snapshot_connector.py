import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class BlockStorageSnapshotsConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_snapshots(self, secret_data: dict, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-block-storage-infrastructure.nhncloudservice.com/v2/{secret_data.get('tenant_id')}/snapshots/detail"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get Block Storage Snapshots. {response.json()}")
            raise Exception(f"Failed to get Block Storage Snapshots. {response.json()}")

        return response.json().get("snapshots", [])