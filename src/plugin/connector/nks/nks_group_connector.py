import logging

import requests

from src.plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class NKSGroupConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_node_group(self, cluster_id: str, secret_data: dict) -> dict:
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

        return response.json()

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

        return response.json()
