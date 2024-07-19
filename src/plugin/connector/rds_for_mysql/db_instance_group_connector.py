import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class DBInstanceGroupConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_db_instance_groups(app_key, user_access_key_id, secret_access_key, region:REGION) -> list:
        db_instance_groups = []

        response = requests.get(
            f"https://{region.name.lower()}-rds-mysql.api.nhncloudservice.com/v3.0/db-instance-groups",
            headers={
                "Content-Type": "application/json",
                "X-TC-APP-KEY": app_key,
                "X-TC-AUTHENTICATION-ID": user_access_key_id,
                "X-TC-AUTHENTICATION-SECRET": secret_access_key
            })

        if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
            _LOGGER.error(f"Failed to get db instance groups. {response.json()}")
            raise Exception(f"Failed to get db instance groups. {response.json()}")

        db_instance_groups.extend(response.json()['dbInstanceGroups'])

        return db_instance_groups