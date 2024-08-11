import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class InstanceConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_servers(self, secret_data: dict, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-instance-infrastructure.nhncloudservice.com/v2/{secret_data.get('tenant_id')}/servers/detail"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get Instances. {response.json()}")
            raise Exception(f"Failed to get Instances. {response.json()}")

        return response.json().get("servers", [])

    def get_volume(self, server_id: str, volume_id: str, secret_data: dict, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-instance-infrastructure.nhncloudservice.com/v2/{secret_data.get('tenant_id')}/servers/{server_id}/os-volume_attachments/{volume_id}"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get Instance's VolumeAttachments. {response.json()}")
            raise Exception(f"Failed to get Instance's VolumeAttachments. {response.json()}")

        return response.json().get("volumeAttachment", [])


    def get_detail(self, secret_data: dict, region: REGION, server_id: str) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-instance-infrastructure.nhncloudservice.com/v2/{secret_data.get('tenant_id')}/servers/{server_id}"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get Instances. {response.json()}")
            raise Exception(f"Failed to get Instances. {response.json()}")

        return response.json().get("server", [])