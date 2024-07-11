import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class UsagePlanConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_usage_plans(app_key, region:REGION) -> list:
        keys = []
        idx = 1
        while True:
            response = requests.get(f"https://{region.name.lower()}-apigateway.api.nhncloudservice.com/v1.0/appkeys/{app_key}/usage-plans?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                _LOGGER.error(f"Failed to get usage plans. {response.json()}")
                raise Exception(f"Failed to get usage plans. {response.json()}")

            if not response.json()['usagePlanList']:
                break

            keys.extend(response.json()['usagePlanList'])
            idx += 1

        return keys