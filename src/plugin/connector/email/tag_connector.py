import logging
import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class TagConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_tags(app_key, secret_key) -> list:
        tags = []
        idx = 1
        while True:
            response = requests.get(
                f"https://email.api.nhncloudservice.com/email/v2.1/appKeys/{app_key}/tags?pageNum={idx}",
                headers={
                    "Content-Type": "application/json",
                    "X-Secret-Key": secret_key
                })

            if response.json().get('header').get('isSuccessful') is False:
                _LOGGER.error(f"Failed to get tags. {response.json()}")
                raise Exception(f"Failed to get tags. {response.json()}")


            if not response.json()['body']['data']:
                break

            tags.extend(response.json()['body']['data'])
            idx += 1

        return tags
