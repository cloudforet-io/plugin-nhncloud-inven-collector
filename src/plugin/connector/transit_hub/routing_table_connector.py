import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class RoutingTableConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_routing_tables(tenant_id, username, password, region:REGION) -> list:
        secret_data = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret_data)
        response = requests.get(f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/transithub_routing_tables",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get routing tables. {response.json()}")
            raise Exception(f"Failed to get routing tables. {response.json()}")

        routing_tables = response.json().get("transithub_routing_tables", [])

        return routing_tables

    @staticmethod
    def get_associations_by_routing_table_id(tenant_id, username, password, routing_table_id, region:REGION) -> list:
        secret_data = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret_data)
        response = requests.get(f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/transithub_routing_associations?routing_table_id={routing_table_id}",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get associations by routing table id. {response.json()}")
            raise Exception(f"Failed to get associations by routing table id. {response.json()}")

        associations = response.json().get("transithub_routing_associations", [])

        return associations

    @staticmethod
    def get_propagations_by_routing_table_id(tenant_id, username, password, routing_table_id, region:REGION) -> list:
        secret_data = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret_data)
        response = requests.get(f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/transithub_routing_propagations?routing_table_id={routing_table_id}",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get propagations by routing table id. {response.json()}")
            raise Exception(f"Failed to get propagations by routing table id. {response.json()}")

        propagations = response.json().get("transithub_routing_propagations", [])

        return propagations

    @staticmethod
    def get_rules_by_routing_table_id(tenant_id, username, password, routing_table_id, region:REGION) -> list:
        secret = {"tenant_id": tenant_id, "username": username, "password": password}
        token = NHNCloudBaseConnector.get_token(secret)
        response = requests.get(f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/gateways/transithub_routing_rules?routing_table_id={routing_table_id}",
                                headers={
                                    "Content-Type": "application/json",
                                    "X-Auth-Token": token,
                                })

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get rules by routing table id. {response.json()}")
            raise Exception(f"Failed to get rules by routing table id. {response.json()}")

        rules = response.json().get("transithub_routing_rules", [])

        return rules