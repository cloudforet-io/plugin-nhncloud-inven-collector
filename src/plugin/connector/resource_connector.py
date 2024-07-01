import logging
from spaceone.core.connector import BaseConnector

_LOGGER = logging.getLogger("cloudforet")


class ResourceConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def list_servers() -> dict:
        return {
            'servers_info': [
                {
                    'id': 'vm-01', 'name': 'ubuntu-server-01', 'ip': '192.168.1.1', 'state': 'running',
                    'account_id': '1234567890', 'created_at': '2024-06-14 08:30:14'
                },
                {
                    'id': 'vm-02', 'name': 'windows-test-vm', 'ip': '10.1.2.3', 'state': 'stopped',
                    'account_id': '1234567890', 'created_at': '2020-06-15 09:30:34'
                }
            ]
        }
