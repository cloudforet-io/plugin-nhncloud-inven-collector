import logging
from spaceone.inventory.plugin.collector.lib import *

from ..base import NHNCloudBaseManager
from ...conf.cloud_service_conf import AUTH_TYPE
from ...connector.email.category_connector import CategoryConnector

_LOGGER = logging.getLogger("cloudforet")


class CategoryManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Email"
        self.cloud_service_type = "Category"
        self.provider = "NHNCloud"
        self.metadata_path = "metadata/email/category.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        category_connector = CategoryConnector()
        categories = category_connector.list_categories(secret_data.get("app_key"), secret_data.get("email_secret_key"))

        for category in categories:
            reference = {
                    "resource_id": category.get("categoryId"),
                    "external_link": "https://github.com/cloudforet-io/plugin-nhncloud-inven-collector"
                    }
            cloud_service = make_cloud_service(
                name=category["categoryName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=category,
                account=secret_data.get("account_id", None),
                reference=reference,
            )

            return cloud_service