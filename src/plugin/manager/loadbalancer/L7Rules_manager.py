import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.loadbalancer.L7Rules_connector import LoadBalancerL7RulesConnector
from plugin.connector.loadbalancer.L7policies_connector import LoadBalancerL7PoliciesConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class LoadBalancerL7RulesManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "LoadBalancer"
        self.cloud_service_type = "L7 Rules"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/loadbalancer/l7rules.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=True,
            is_major=True,
            tags={
                "spaceone:icon": f"{ASSET_URL}/load_balancer.png"
            },
            labels=["Networking"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        policies_connector = LoadBalancerL7PoliciesConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = policies_connector.get_policies(secret_data, AVAILABLE_REGION)
            for resource in resources:
                policy_id = resource['id']
                rules_connector = LoadBalancerL7RulesConnector()
                rules = rules_connector.get_rules(secret_data, policy_id, AVAILABLE_REGION)
                for rule in rules:
                    reference = {
                        "resource_id": rule.get("id")
                    }
                    cloud_service = make_cloud_service(
                        name=rule['id'],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=rule,
                        account=secret_data.get("username", None),
                        reference=reference,
                        region_code=AVAILABLE_REGION.name
                    )
                    yield cloud_service