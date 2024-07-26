import logging
import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")

class CertificateConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_certificates(app_key, user_access_key_id, secret_access_key) -> list:
        certificates = []
        current_page = 1

        while True:
            response = requests.get(
                f"https://certmanager.api.nhncloudservice.com/certmanager/v1.1/appkeys/{app_key}/certificates",
                headers={
                    "Content-Type": "application/json",
                    "X-TC-AUTHENTICATION-ID": user_access_key_id,
                    "X-TC-AUTHENTICATION-SECRET": secret_access_key
                },
                params={
                    "pageNum": current_page,
                    "pageSize": 10 # defalut
                })

            response_data = response.json()
            data = response_data['body']['data']

            if not data:
                break

            certificates.extend(data)
            current_page += 1
            total_pages = response_data['body']['totalPage']

            if current_page > total_pages:
                break

        return certificates
