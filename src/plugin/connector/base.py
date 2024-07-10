from spaceone.core.connector import BaseConnector


class NHNCloudBaseConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)