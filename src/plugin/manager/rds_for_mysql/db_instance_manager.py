import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL, REGION
from plugin.connector.rds_for_mysql.db_instance_connector import DBInstanceConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class DBInstanceManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "RDS for MySQL"
        self.cloud_service_type = "DB Instance"
        self.metadata_path = f"metadata/{self.cloud_service_group.replace(' ', '_').lower()}/{self.cloud_service_type.replace(' ', '_').lower()}.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/rds_for_mysql.png"
            },
            labels=["Database"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        db_instance_connector = DBInstanceConnector()
        
        db_instances = []
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            if (secret_data.get("user_access_key_id") is not None and 
                secret_data.get("secret_access_key") is not None):
                db_instances = db_instance_connector.list_db_instances(secret_data.get("app_key"), secret_data.get("user_access_key_id"), secret_data.get("secret_access_key"), AVAILABLE_REGION)
            for db_instance in db_instances:
                reference = {
                    "resource_id": db_instance.get("dbInstanceId"),
                    "external_link": ""
                }
                
                schemas = db_instance_connector.list_schemas_by_db_instance_id(secret_data.get("app_key"), secret_data.get("user_access_key_id"), secret_data.get("secret_access_key"), db_instance.get("dbInstanceId"), AVAILABLE_REGION)
                users = db_instance_connector.list_users_by_db_instance_id(secret_data.get("app_key"), secret_data.get("user_access_key_id"), secret_data.get("secret_access_key"), db_instance.get("dbInstanceId"), AVAILABLE_REGION)
                db_instance["schemas"] = schemas
                db_instance["users"] = users
                
                cloud_service = make_cloud_service(
                    name=db_instance["dbInstanceName"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=db_instance,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )

                yield cloud_service