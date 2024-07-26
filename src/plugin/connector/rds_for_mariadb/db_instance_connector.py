import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class DBInstanceConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_users_by_db_instance_id(app_key, user_access_key_id, secret_access_key, db_instance_id, region:REGION) -> list:
        users = []

        response = requests.get(f"https://{region.name.lower()}-rds-mariadb.api.nhncloudservice.com/v3.0/db-instances/{db_instance_id}/db-users",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-TC-APP-KEY": app_key,
                                    "X-TC-AUTHENTICATION-ID": user_access_key_id,
                                    "X-TC-AUTHENTICATION-SECRET": secret_access_key
                                })

        if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
            _LOGGER.error(f"Failed to get DB users. {response.json()}")
            raise Exception(f"Failed to get DB users. {response.json()}")

        users.extend(response.json()["dbUsers"])

        return users
    
    
    @staticmethod
    def list_schemas_by_db_instance_id(app_key, user_access_key_id, secret_access_key, db_instance_id, region:REGION) -> list:
        schemas = []

        response = requests.get(f"https://{region.name.lower()}-rds-mariadb.api.nhncloudservice.com/v3.0/db-instances/{db_instance_id}/db-schemas",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-TC-APP-KEY": app_key,
                                    "X-TC-AUTHENTICATION-ID": user_access_key_id,
                                    "X-TC-AUTHENTICATION-SECRET": secret_access_key
                                })

        if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
            _LOGGER.error(f"Failed to get DB schemas. {response.json()}")
            raise Exception(f"Failed to get DB schemas. {response.json()}")

        schemas.extend(response.json()["dbSchemas"])

        return schemas


    @staticmethod
    def list_db_instances(app_key, user_access_key_id, secret_access_key, region:REGION) -> list:
        db_instances = []

        response = requests.get(
            f"https://{region.name.lower()}-rds-mariadb.api.nhncloudservice.com/v3.0/db-instances",
            headers={
                "Content-Type": "application/json",
                "X-TC-APP-KEY": app_key,
                "X-TC-AUTHENTICATION-ID": user_access_key_id,
                "X-TC-AUTHENTICATION-SECRET": secret_access_key
            })

        if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
            _LOGGER.error(f"Failed to get db instances. {response.json()}")
            raise Exception(f"Failed to get db instances. {response.json()}")

        db_instances.extend(response.json()['dbInstances'])

        return db_instances