import logging

import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger('cloudforet')

class GSLBConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_gslbs(app_key) -> list:
        gslbs = []
        idx = 1
        while True:
            response = requests.get(f"https://dnsplus.api.nhncloudservice.com/dnsplus/v1.0/appkeys/{app_key}/gslbs?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                # Ignore collecting request when the service is inactivated. This logic does not ensure that app key is valid.
                if response.json().get('header').get('resultCode') == 4010001:
                    return []

                _LOGGER.error(f"Failed to get GSLBs. {response.json()}")
                raise Exception(f"Failed to get GSLBs. {response.json()}")

            if not response.json()['gslbList']:
                break

            gslbs.extend(response.json()['gslbList'])
            idx += 1

        return gslbs