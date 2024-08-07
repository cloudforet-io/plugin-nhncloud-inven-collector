import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.transit_hub.routing_table_connector import RoutingTableConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger('cloudforet')

class RoutingTableManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "Transit Hub"
        self.cloud_service_type = "Routing Table"
        self.metadata_path = f"metadata/{self.cloud_service_group.replace(' ', '_').lower()}/{self.cloud_service_type.replace(' ', '_').lower()}.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=False,
            is_major=False,
            tags={
                "spaceone:icon": f"{ASSET_URL}/transit_hub.png"
            },
            labels=["Networking"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        routing_table_connector = RoutingTableConnector()

        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            routing_tables = routing_table_connector.list_routing_tables(secret_data.get("tenant_id"), secret_data.get("username"), secret_data.get("password"), AVAILABLE_REGION)
            for routing_table in routing_tables:
                routing_associations = routing_table_connector.get_associations_by_routing_table_id(secret_data.get("tenant_id"), secret_data.get("username"), secret_data.get("password"), routing_table.get("id"), AVAILABLE_REGION)
                routing_table["associations"] = routing_associations

                routing_propagations = routing_table_connector.get_propagations_by_routing_table_id(secret_data.get("tenant_id"), secret_data.get("username"), secret_data.get("password"), routing_table.get("id"), AVAILABLE_REGION)
                routing_table["propagations"] = routing_propagations

                routing_rules = routing_table_connector.get_rules_by_routing_table_id(secret_data.get("tenant_id"), secret_data.get("username"), secret_data.get("password"), routing_table.get("id"), AVAILABLE_REGION)
                routing_table["rules"] = routing_rules

                reference = {
                    "resource_id": routing_table.get("id"),
                    "external_link": ""
                }

                cloud_service = make_cloud_service(
                    name=routing_table["name"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=routing_table,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )
                yield cloud_service