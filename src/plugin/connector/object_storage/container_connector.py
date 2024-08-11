import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class ContainerConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_containers(self, secret_data: dict, region: REGION) -> list:
        token = self.get_token(secret_data)
        containers = []

        url = f"https://{region.name.lower()}-api-object-storage.nhncloudservice.com/v1/{secret_data.get('storage_account')}?format=json"
        headers = {"X-Auth-Token": token}
        response = requests.get(url, headers=headers)
        
        containers.extend(response.json())

        return containers
