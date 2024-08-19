import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class ParameterGroupConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_parameter_groups(app_key, user_access_key_id, secret_access_key, region:REGION) -> list:
        parameter_groups = []

        response = requests.get(
            f"https://{region.name.lower()}-rds-mariadb.api.nhncloudservice.com/v3.0/parameter-groups",
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

            _LOGGER.error(f"Failed to get parameter groups. {response.json()}")
            raise Exception(f"Failed to get parameter groups. {response.json()}")

        parameter_groups.extend(response.json()['parameterGroups'])

        return parameter_groups