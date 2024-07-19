import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class AttachmentConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_attachments(tenant_id, username, password, region:REGION) -> list:
        secret_data = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret_data)
        response = requests.get(f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/transithub_attachments",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get attachments. {response.json()}")
            raise Exception(f"Failed to get attachments. {response.json()}")

        attachments = response.json().get("transithub_attachments", [])

        return attachments