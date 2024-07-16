import json

import requests
from spaceone.core.connector import BaseConnector


class NHNCloudBaseConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_token(secret_data: dict) -> dict:
        params = {
            "auth": {
                "tenantId": secret_data.get('tenant_id'),
                "passwordCredentials": {
                    "username": secret_data.get('username'),
                    "password": secret_data.get('password')
                }
            }
        }
        response = requests.post("https://api-identity-infrastructure.nhncloudservice.com/v2.0/tokens", json=params)
        response_dict = json.loads(response.content)
        token = response_dict['access']['token']['id']
        return token