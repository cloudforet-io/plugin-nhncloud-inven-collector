import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL
from plugin.connector.push.token_connector import PushTokenConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class PushTokenManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Push"
        self.cloud_service_type = "Token"
        self.metadata_path = f"metadata/{self.cloud_service_group.lower()}/{self.cloud_service_type.lower()}.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/push.png"
            },
            labels=["Application Integration"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        token_connector = PushTokenConnector()

        tokens = []
        if hasattr(secret_data, "push_secret_key"):
            tokens = token_connector.list_tokens(secret_data.get("app_key"), secret_data.get("push_secret_key"))

        for token in tokens:
            reference = {
                    "resource_id": token.get("token"),
                    "external_link": ""
                    }

            cloud_service = make_cloud_service(
                name=token["uid"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=token,
                account=secret_data.get("project_id"),
                reference=reference,
            )

            yield cloud_service