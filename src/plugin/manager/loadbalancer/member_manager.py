import logging
from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, REGION, ASSET_URL
from plugin.connector.loadbalancer.member_connector import LoadBalancerMemberConnector
from plugin.connector.loadbalancer.pools_connector import LoadBalancerPoolsConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class LoadBalancerMemberManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.TOKEN
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cloud_service_group = "LoadBalancer"
        self.cloud_service_type = "Members"
        self.provider = "nhncloud"
        self.metadata_path = "metadata/loadbalancer/members.yaml"

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
        pools_connector = LoadBalancerPoolsConnector()
        members_connector = LoadBalancerMemberConnector()
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            resources = pools_connector.get_pools(secret_data, AVAILABLE_REGION)
            for resource in resources:
                pool_id = resource['id']
                members = members_connector.get_members(secret_data, pool_id, AVAILABLE_REGION)
                for member in members:
                    reference = {
                        "resource_id": member.get("id")
                    }
                    cloud_service = make_cloud_service(
                        name=member['id'],
                        cloud_service_type=self.cloud_service_type,
                        cloud_service_group=self.cloud_service_group,
                        provider=self.provider,
                        data=member,
                        account=secret_data.get("username", None),
                        reference=reference,
                        region_code=AVAILABLE_REGION.name
                    )
                    yield cloud_service
