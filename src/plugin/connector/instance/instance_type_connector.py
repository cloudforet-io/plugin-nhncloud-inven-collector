import logging

import requests

from src.plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class InstanceTypeConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_types(self, secret_data: dict) -> dict:
        token = self.get_token(secret_data)

        url = ("https://kr1-api-instance-infrastructure.nhncloudservice.com/v2/"
               + secret_data.get('tenant_id') + "/flavors")
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        return response.json()