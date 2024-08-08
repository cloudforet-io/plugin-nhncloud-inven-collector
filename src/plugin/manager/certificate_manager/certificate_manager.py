import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL
from plugin.connector.certificate_manager.certificate_connector import CertificateConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class CertificateManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Certificate Manager"
        self.cloud_service_type = "Certificate"
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
                "spaceone:icon": f"{ASSET_URL}/certificate_manager.png"
            },
            labels=["Management", "Security", "Networking"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        certificate_connector = CertificateConnector()
        certificates = []

        if (secret_data.get("certificate_app_key") is not None and 
            secret_data.get("user_access_key_id") is not None and 
            secret_data.get("secret_access_key") is not None):
            certificates = certificate_connector.list_certificates(secret_data.get("certificate_app_key"), secret_data.get("user_access_key_id"), secret_data.get("secret_access_key"))

        for certificate in certificates:
            reference = {
                    "resource_id": certificate.get("certificateName"),
                    "external_link": ""
                    }
            cloud_service = make_cloud_service(
                name=certificate["certificateName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=certificate,
                account=secret_data.get("project_id"),
                reference=reference,
            )

            yield cloud_service