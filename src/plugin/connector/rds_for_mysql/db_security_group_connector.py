import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class DBSecurityGroupConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_db_security_groups(app_key, user_access_key_id, secret_access_key, region:REGION) -> list:
        db_security_groups = []

        response = requests.get(
            f"https://{region.name.lower()}-rds-mysql.api.nhncloudservice.com/v3.0/db-security-groups",
            headers={
                "Content-Type": "application/json",
                "X-TC-APP-KEY": app_key,
                "X-TC-AUTHENTICATION-ID": user_access_key_id,
                "X-TC-AUTHENTICATION-SECRET": secret_access_key
            })

        if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
            _LOGGER.error(f"Failed to get db security groups. {response.json()}")
            raise Exception(f"Failed to get db security groups. {response.json()}")

        db_security_groups.extend(response.json()['dbSecurityGroups'])

        return db_security_groups