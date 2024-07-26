import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class VPCSubnetConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_subnet(self, secret_data: dict, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/vpcsubnets"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get Subnets. {response.json()}")
            raise Exception(f"Failed to get Subnets. {response.json()}")

        return response.json().get("vpcsubnets", [])