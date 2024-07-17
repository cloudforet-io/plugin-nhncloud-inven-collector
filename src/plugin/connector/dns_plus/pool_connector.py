import logging

import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger('cloudforet')

class PoolConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_pools(app_key) -> list:
        pools = []
        idx = 1
        while True:
            response = requests.get(f"https://dnsplus.api.nhncloudservice.com/dnsplus/v1.0/appkeys/{app_key}/pools?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                _LOGGER.error(f"Failed to get pools. {response.json()}")
                raise Exception(f"Failed to get pools. {response.json()}")

            if not response.json()['poolList']:
                break

            pools.extend(response.json()['poolList'])
            idx += 1

        return pools