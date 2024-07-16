import logging
import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class TemplateConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_templates(app_key, secret_key) -> list:
        templates = []
        idx = 1
        while True:
            response = requests.get(
                f"https://email.api.nhncloudservice.com/email/v2.1/appKeys/{app_key}/templates?pageNum={idx}",
                headers={
                    "Content-Type": "application/json",
                    "X-Secret-Key": secret_key
                })

            if response.json().get('header').get('isSuccessful') is False:
                _LOGGER.error(f"Failed to get templates. {response.json()}")
                raise Exception(f"Failed to get templates. {response.json()}")


            if not response.json()['body']['data']:
                break

            templates.extend(response.json()['body']['data'])
            idx += 1

        return templates
