import logging

import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger('cloudforet')

class HealthCheckConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_health_checks(app_key) -> list:
        health_checks = []
        idx = 1
        while True:
            response = requests.get(f"https://dnsplus.api.nhncloudservice.com/dnsplus/v1.0/appkeys/{app_key}/health-checks?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                # Ignore collecting request when the service is inactivated. This logic does not ensure that app key is valid.
                if response.json().get('header').get('resultCode') == 4010001:
                    return []

                _LOGGER.error(f"Failed to get Health Checks. {response.json()}")
                raise Exception(f"Failed to get Health Checks. {response.json()}")

            if not response.json()['healthCheckList']:
                break

            health_checks.extend(response.json()['healthCheckList'])
            idx += 1

        return health_checks