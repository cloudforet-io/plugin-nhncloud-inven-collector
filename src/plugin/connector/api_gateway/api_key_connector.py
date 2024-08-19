import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class APIKeyConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_keys(app_key, region:REGION) -> list:
        keys = []
        idx = 1
        while True:
            response = requests.get(f"https://{region.name.lower()}-apigateway.api.nhncloudservice.com/v1.0/appkeys/{app_key}/apikeys?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                # Ignore collecting request when the service is inactivated. This logic does not ensure that app key is valid.
                if response.json().get('header').get('resultCode') == 401199000:
                    return []
                _LOGGER.error(f"Failed to get keys. {response.json()}")
                raise Exception(f"Failed to get keys. {response.json()}")

            if not response.json()['apiKeyList']:
                break

            keys.extend(response.json()['apiKeyList'])
            idx += 1

        return keys