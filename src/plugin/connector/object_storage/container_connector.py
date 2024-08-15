import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class ContainerConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_containers(tenant_id, username, password, storage_account, region: REGION) -> list:
        secret_data = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret_data)
        response = requests.get(f"https://{region.name.lower()}-api-object-storage.nhncloudservice.com/v1/{storage_account}?format=json",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get containers. {response.json()}")
            raise Exception(f"Failed to get containers. {response.json()}")

        containers = response.json()

        return containers