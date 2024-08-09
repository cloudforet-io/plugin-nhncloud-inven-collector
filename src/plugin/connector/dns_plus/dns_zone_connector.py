import logging

import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class DNSZoneConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_dns_zones(app_key) -> list:
        zones = []
        idx = 1
        while True:
            response = requests.get(f"https://dnsplus.api.nhncloudservice.com/dnsplus/v1.0/appkeys/{app_key}/zones?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                # Ignore collecting request when the service is inactivated. This logic does not ensure that app key is valid.
                if response.json().get('header').get('resultCode') == 4010001:
                    return []

                _LOGGER.error(f"Failed to get zones. {response.json()}")
                raise Exception(f"Failed to get zones. {response.json()}")

            if not response.json()['zoneList']:
                break

            zones.extend(response.json()['zoneList'])
            idx += 1

        return zones

    @staticmethod
    def get_record_sets_by_zone_id(app_key, zone_id) -> list:
        record_sets = []
        idx = 1
        while True:
            response = requests.get(f"https://dnsplus.api.nhncloudservice.com/dnsplus/v1.0/appkeys/{app_key}/zones/{zone_id}/recordsets?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                _LOGGER.error(f"Failed to get record sets. {response.json()}")
                raise Exception(f"Failed to get record sets. {response.json()}")

            if not response.json()['recordsetList']:
                break

            record_sets.extend(response.json()['recordsetList'])
            idx += 1

        return record_sets

