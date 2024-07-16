import logging
import requests

from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class PushTokenConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_tokens(app_key, secret_key) -> list:
        tokens = []
        cursor_uid = None
        cursor_token = None

        while True:
            response = None
            if cursor_uid is None and cursor_token is None:
                response = requests.get(f"https://api-push.cloud.toast.com/push/v2.4/appkeys/{app_key}/tokens-by-cursor",
                                        headers={
                                            "Content-Type": "application/json",
                                            "X-Secret-Key": secret_key
                                        })
            else:
                response = requests.get(f"https://api-push.cloud.toast.com/push/v2.4/appkeys/{app_key}/tokens-by-cursor?cursorUid={cursor_uid}&cursorToken={cursor_token}",
                                        headers={
                                            "Content-Type": "application/json",
                                            "X-Secret-Key": secret_key
                                        })

            if response.json().get('header').get('isSuccessful') is False:
                _LOGGER.error(f"Failed to get tokens. {response.json()}")
                raise Exception(f"Failed to get tokens. {response.json()}")

            if not response.json()['tokens']:
                break

            partial_tokens = response.json()['tokens']
            tokens.extend(partial_tokens)
            cursor_uid = partial_tokens[-1]['uid']
            cursor_token = partial_tokens[-1]['token']

        return tokens