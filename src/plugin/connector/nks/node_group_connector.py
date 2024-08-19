import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class NodeGroupConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_node_group(self, secret_data: dict, cluster_id: str, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = ("https://kr1-api-kubernetes-infrastructure.nhncloudservice.com/v1/clusters/" +
               cluster_id + "/nodegroups")
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "OpenStack-API-Version": "container-infra latest",
            "X-Auth-Token": token
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get NKS Groups. {response.json()}")
            raise Exception(f"Failed to get NKS Groups. {response.json()}")

        return response.json().get("nodegroups", [])

    def get_node_group_detail(self, cluster_id: str, node_group_name: str, secret_data: dict) -> dict:
        token = self.get_token(secret_data)

        url = ("https://kr1-api-kubernetes-infrastructure.nhncloudservice.com/v1/clusters/" +
               cluster_id + "/nodegroups/" + node_group_name)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "OpenStack-API-Version": "container-infra latest",
            "X-Auth-Token": token
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get NKS Group Detail. {response.json()}")
            raise Exception(f"Failed to get NKS Group Detail. {response.json()}")

        return response.json()
