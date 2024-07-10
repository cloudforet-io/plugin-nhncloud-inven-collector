import logging
from spaceone.inventory.plugin.collector.lib import *

from src.plugin.conf.cloud_service_conf import AUTH_TYPE
from src.plugin.connector.instance.keypair_connector import KeyPairConnector
from src.plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class KeyPairManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "Instance"
        self.cloud_service_type = "KeyPair"
        self.provider = "NHNCloud"
        self.metadata_path = "metadata/resource/instance/keypair.yaml"

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
        keypair_connector = KeyPairConnector()
        resources = keypair_connector.get_keypair(secret_data)
        for resource in resources['keypairs']:
            detail = keypair_connector.get_keypair_detail(secret_data, resource['keypair']['name'])['keypair']
            reference = {
                "resource_id": resource.get("name"),
                "external_link": "https://github.com/cloudforet-io/plugin-nhncloud-inven-collector"
            }
            # {'public_key': 'ssh-rsa xxx Generated-by-Nova', 'user_id': '293c075e1229440982aed9b1b690718d', 'name': 'test2', 'deleted': False, 'created_at': '2024-07-09T04:57:45.000000', 'updated_at': None, 'fingerprint': '58:4a:92:18:55:8e:e2:8b:5e:ba:5e:ee:b6:b1:8a:a7', 'deleted_at': None, 'id': 34142}
            cloud_service = make_cloud_service(
                name=detail['name'],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=detail,
                account=secret_data.get("username", None),
                reference=reference,
            )
            yield make_response(
                cloud_service=cloud_service,
                match_keys=[["name", "reference.resource_id", "account", "provider"]],
            )
