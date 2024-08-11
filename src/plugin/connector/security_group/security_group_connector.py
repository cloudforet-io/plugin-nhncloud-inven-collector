import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class SGConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_security_groups(self, secret_data: dict, region: REGION, name: str = None) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/security-groups?tenant_id={secret_data.get('tenant_id')}"

        # name이 제공되었으면 쿼리 파라미터에 추가
        if name:
            url += f"&name={name}"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            _LOGGER.error(f"Failed to get Security Groups. {response.json()}")
            raise Exception(f"Failed to get Security Groups. {response.json()}")

        return response.json().get("security_groups", [])