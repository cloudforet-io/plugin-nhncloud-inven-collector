import logging
import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class CategoryConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_categories(app_key, secret_key) -> list:
        categories = []
        idx = 1
        while True:
            response = requests.get(
                f"https://email.api.nhncloudservice.com/email/v2.1/appKeys/{app_key}/categories?pageNum={idx}",
                headers={
                    "Content-Type": "application/json",
                    "X-Secret-Key": secret_key
                })

            if not response.json()['body']['data']:
                break

            categories.extend(response.json()['body']['data'])
            idx += 1

        return categories
