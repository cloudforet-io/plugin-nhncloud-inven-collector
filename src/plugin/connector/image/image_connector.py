import logging

import requests

from src.plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class ImageConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_image(self, secret_data: dict) -> dict:
        token = self.get_token(secret_data)

        url = "https://kr1-api-image-infrastructure.nhncloudservice.com/v2/images?owner=" + secret_data['tenant_id']
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        return response.json()