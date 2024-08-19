import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class BackupConnector(NHNCloudBaseConnector):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_backups(app_key, user_access_key_id, secret_access_key, region:REGION) -> list:
        backups = []
        idx = 1
        while True:
            response = requests.get(
                f"https://{region.name.lower()}-rds-mariadb.api.nhncloudservice.com/v3.0/backups?page={idx}&size=10",
                headers={
                    "Content-Type": "application/json",
                    "X-TC-APP-KEY": app_key,
                    "X-TC-AUTHENTICATION-ID": user_access_key_id,
                    "X-TC-AUTHENTICATION-SECRET": secret_access_key
                })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                # Ignore collecting request when the service is inactivated. This logic does not ensure that app key is valid.
                if response.json().get('header').get('resultCode') == 4005:
                    return []

                _LOGGER.error(f"Failed to get Backups. {response.json()}")
                raise Exception(f"Failed to get Backups. {response.json()}")


            if not response.json()['backups']:
                break

            backups.extend(response.json()['backups'])
            idx += 1
            
        return backups