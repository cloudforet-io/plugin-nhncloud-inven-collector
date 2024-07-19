import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class ServiceGatewayConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_gateways(self, secret_data: dict, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/servicegateways"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get Service Gateways. {response.json()}")
            raise Exception(f"Failed to get Service Gateways. {response.json()}")

        return response.json().get("servicegateways", [])

    def get_detail(self, secret_data: dict, service_gateway_id: str, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/servicegateways/{service_gateway_id}"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get Service Gateway Details. {response.json()}")
            raise Exception(f"Failed to get Service Gateway Details. {response.json()}")

        return response.json().get("servicegateway", [])
