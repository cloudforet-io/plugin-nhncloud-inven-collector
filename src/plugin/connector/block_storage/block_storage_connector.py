import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class BlockStorageConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_volumes(self, secret_data: dict, region: REGION) -> list:
        token = self.get_token(secret_data)

        volumes = []
        offset = 0  # limit 처리위해

        while True:
            url = f"https://{region.name.lower()}-api-block-storage-infrastructure.nhncloudservice.com/v2/{secret_data.get('tenant_id')}/volumes/detail?offset={offset}"
            headers = {"X-Auth-Token": token}

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                _LOGGER.error(f"Failed to get Block Storage Volumes. {response.json()}")
                raise Exception(f"Failed to get Block Storage Volumes. {response.json()}")

            if not response.json()['volumes']:
                break

            volumes.extend(response.json()['volumes'])
            offset += 1000

            if offset > 100000:  # 무한루프 처리
                break

        return volumes
