import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL
from plugin.connector.email.template_connector import TemplateConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class TemplateManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Email"
        self.cloud_service_type = "Template"
        self.metadata_path = f"metadata/{self.cloud_service_group.lower()}/{self.cloud_service_type.lower()}.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=False,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/email.png"
            },
            labels=["Application Integration"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        template_connector = TemplateConnector()

        templates = []
        if hasattr(secret_data, "email_secret_key"):
            templates = template_connector.list_templates(secret_data.get("app_key"), secret_data.get("email_secret_key"))

        for template in templates:
            reference = {
                    "resource_id": template.get("templateId"),
                    "external_link": ""
                    }
            cloud_service = make_cloud_service(
                name=template["templateName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=template,
                account=secret_data.get("project_id"),
                reference=reference,
            )

            yield cloud_service