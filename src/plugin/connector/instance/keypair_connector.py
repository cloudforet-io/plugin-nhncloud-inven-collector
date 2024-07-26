import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class KeyPairConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_keypair(self, secret_data: dict, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-instance-infrastructure.nhncloudservice.com/v2/{secret_data.get('tenant_id')}/os-keypairs"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get keypairs. {response.json()}")
            raise Exception(f"Failed to get keypairs. {response.json()}")

        return response.json().get("keypairs", [])

    def get_keypair_detail(self, secret_data: dict, keypair_name: str, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-instance-infrastructure.nhncloudservice.com/v2/{secret_data.get('tenant_id')}/os-keypairs/{keypair_name}"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get keypair Details. {response.json()}")
            raise Exception(f"Failed to get keypair Details. {response.json()}")

        return response.json().get("keypair", [])