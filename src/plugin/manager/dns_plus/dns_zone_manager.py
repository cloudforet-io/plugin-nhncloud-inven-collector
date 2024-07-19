import logging

from spaceone.inventory.plugin.collector.lib import make_cloud_service_type, make_cloud_service

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL
from plugin.connector.dns_plus.dns_zone_connector import DNSZoneConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")

class DNSZoneManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "DNS Plus"
        self.cloud_service_type = "DNS Zone"
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
                "spaceone:icon": f"{ASSET_URL}/dns_plus.png"
            }
        )
        return cloud_service_type

    def create_cloud_service(self, secret_data):
        dns_zone_connector = DNSZoneConnector()

        zones = dns_zone_connector.list_dns_zones(secret_data.get("app_key"))
        for zone in zones:
            reference = {
                "resource_id": zone.get("zoneId"),
                "external_link": ""
            }

            record_sets = dns_zone_connector.get_record_sets_by_zone_id(secret_data.get("app_key"), zone.get("zoneId"))
            for record_set in record_sets:
                record_list = record_set.get("recordList", [])
                record_set["recordList"] = list(map(lambda x : x['recordContent'], record_list))

            zone["recordSets"] = record_sets

            cloud_service = make_cloud_service(
                name=zone["zoneName"],
                cloud_service_type=self.cloud_service_type,
                cloud_service_group=self.cloud_service_group,
                provider=self.provider,
                data=zone,
                account=secret_data.get("project_id"),
                reference=reference
            )
            yield cloud_service