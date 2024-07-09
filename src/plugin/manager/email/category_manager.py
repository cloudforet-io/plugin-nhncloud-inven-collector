import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE
from plugin.connector.email.category_connector import CategoryConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class CategoryManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Email"
        self.cloud_service_type = "Category"
        self.metadata_path = "metadata/email/category.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=False,
            is_major=False,
            tags={
                "spaceone:icon": "https://raw.githubusercontent.com/cloudforet-io/static-assets/master/providers/nhncloud/email.png"
            }
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        category_connector = CategoryConnector()
        categories = category_connector.list_categories(secret_data.get("app_key"), secret_data.get("email_secret_key"))

        for category in categories:
            reference = {
                    "resource_id": category.get("categoryId"),
                    "external_link": f"https://cloudforet-dev.console.nhncloud.com/project/{secret_data.get('project_id')}/notification/email#manage-templates"
                    }
            cloud_service = make_cloud_service(
                name=category["categoryName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=category,
                account=secret_data.get("project_id"),
                reference=reference,
            )

            yield cloud_service