import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class MulticastDomainConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_multicast_domains(tenant_id, username, password, region:REGION) -> list:
        secret_data = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret_data)
        response = requests.get(f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/transithub_multicast_domains",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get multicast domains. {response.json()}")
            raise Exception(f"Failed to get multicast domains. {response.json()}")

        multicast_domains = response.json().get("transithub_multicast_domains", [])

        return multicast_domains

    @staticmethod
    def get_multicast_associations_by_multicast_domain_id(tenant_id, username, password, multicast_domain_id, region:REGION) -> list:
        secret_data = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret_data)
        response = requests.get(f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/transithub_multicast_associations?domain_id={multicast_domain_id}",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get associations by multicast domain id. {response.json()}")
            raise Exception(f"Failed to get associations by multicast domain id. {response.json()}")

        associations = response.json().get("transithub_multicast_associations", [])

        return associations

    @staticmethod
    def get_multicast_groups_by_multicast_domain_id(tenant_id, username, password, multicast_domain_id, region:REGION) -> list:
        secret_data = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret_data)
        response = requests.get(f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/transithub_multicast_groups?domain_id={multicast_domain_id}",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get multicast groups by multicast domain id. {response.json()}")
            raise Exception(f"Failed to get multicast groups by multicast domain id. {response.json()}")

        multicast_groups = response.json().get("transithub_multicast_groups", [])

        return multicast_groups