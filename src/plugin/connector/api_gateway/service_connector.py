import logging

import requests

from plugin.conf.cloud_service_conf import REGION, HTTP_METHODS
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class APIGatewayServiceConnector(NHNCloudBaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_stages_by_service_id(app_key, service_id, region:REGION) -> list:
        stages = []
        idx = 1
        while True:
            response = requests.get(f"https://{region.name.lower()}-apigateway.api.nhncloudservice.com/v1.0/appkeys/{app_key}/services/{service_id}/stages?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                _LOGGER.error(f"Failed to get stages. {response.json()}")
                raise Exception(f"Failed to get stages. {response.json()}")

            if not response.json()['stageList']:
                break

            stages.extend(response.json()['stageList'])
            idx += 1

        return stages

    @staticmethod
    def list_resources_by_service_id(app_key, service_id, region:REGION) -> list:
        resources = []
        response = requests.get(f"https://{region.name.lower()}-apigateway.api.nhncloudservice.com/v1.0/appkeys/{app_key}/services/{service_id}/resources",
                                headers={
                                    "Content-Type": "application/json",
                                })

        if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
            _LOGGER.error(f"Failed to get resources. {response.json()}")
            raise Exception(f"Failed to get resources. {response.json()}")

        for resource in response.json()['resourceList']:
            if resource.get('methodType') not in HTTP_METHODS:
                continue

            resources.append(resource)

        return resources

    @staticmethod
    def list_services(app_key, region:REGION) -> list:
        services = []
        idx = 1
        while True:
            response = requests.get(f"https://{region.name.lower()}-apigateway.api.nhncloudservice.com/v1.0/appkeys/{app_key}/services?page={idx}",
                                    headers={
                                        "Content-Type": "application/json",
                                    })

            if response.status_code != 200 or response.json().get('header').get('isSuccessful') is False:
                _LOGGER.error(f"Failed to get services. {response.json()}")
                raise Exception(f"Failed to get services. {response.json()}")

            if not response.json()['apigwServiceList']:
                break

            services.extend(response.json()['apigwServiceList'])
            idx += 1

        return services