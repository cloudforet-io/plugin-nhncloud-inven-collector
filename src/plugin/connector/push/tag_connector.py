import logging

import requests

from plugin.conf.cloud_service_conf import REGION, HTTP_METHODS
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class PushTagConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_tags(app_key, secret_key) -> list:
        response = requests.get(f"https://api-push.cloud.toast.com/push/v2.4/appkeys/{app_key}/tags",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Secret-Key": secret_key
                                })

        if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
            _LOGGER.error(f"Failed to get tags. {response.json()}")
            raise Exception(f"Failed to get tags. {response.json()}")

        tags = response.json()['tags']

        return tags