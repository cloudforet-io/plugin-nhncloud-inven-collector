import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class NKSConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_cluster(self, secret_data: dict, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-kubernetes-infrastructure.nhncloudservice.com/v1/clusters"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "OpenStack-API-Version": "container-infra latest",
            "X-Auth-Token": token
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            _LOGGER.error(f"Failed to get NKS Clusters. {response.json()}")
            raise Exception(f"Failed to get NKS Clusters. {response.json()}")

        return response.json().get("clusters", [])
