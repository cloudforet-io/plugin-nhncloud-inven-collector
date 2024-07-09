import abc
import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.plugin.collector.lib import *
from plugin.conf.cloud_service_conf import AUTH_TYPE, PROVIDER_NAME

_LOGGER = logging.getLogger("cloudforet")


class NHNCloudBaseManager(BaseManager):
    service: str = None
    cloud_service_group: str = None
    cloud_service_type: str = None
    auth_type: AUTH_TYPE = None
    required_properties = ["service", "cloud_service_group", "cloud_service_type", "auth_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider = PROVIDER_NAME


    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for required_property in cls.required_properties:
            if not hasattr(cls, required_property):
                raise NotImplementedError(f"Attribute {required_property} must be defined in subclass.")

    @abc.abstractmethod
    def create_cloud_service_type(self):
        raise NotImplementedError(
            "method `create_cloud_service_type` should be implemented"
        )

    @abc.abstractmethod
    def create_cloud_service(self, secret_data):
        raise NotImplementedError("method `create_cloud_service` should be implemented")

    @classmethod
    def list_managers_by_schema(cls, schema: str):
        for manager in cls.__subclasses__():

            if manager.auth_type.value == schema:
                yield manager

    @staticmethod
    def get_auth_type_by_secret_data(secret_data:dict):
        if 'tenant_id' in secret_data and 'username' in secret_data and 'password' in secret_data:
            return AUTH_TYPE.TOKEN
        if 'app_key' in secret_data:
            return AUTH_TYPE.APP_KEY

        raise NotImplementedError("Secret data is not valid")

    def collect_resources(self, secret_data: dict):
        try:
            yield from self.collect_cloud_service_type()

            cloud_services = self.collect_cloud_service(
                secret_data
            )
            for cloud_service in cloud_services:
                yield cloud_service

        except Exception as e:
            yield make_error_response(
                error=e,
                provider=self.provider,
                cloud_service_group=self.cloud_service_group,
                cloud_service_type=self.cloud_service_type,
            )

    def collect_cloud_service_type(self):
        cloud_service_type = self.create_cloud_service_type()

        yield make_response(
            cloud_service_type=cloud_service_type,
            match_keys=[["name", "reference.resource_id", "account", "provider"]],
            resource_type="inventory.CloudServiceType",
        )

    def collect_cloud_service(self, secret_data: dict):
        total_resources = []

        cloud_services = self.create_cloud_service(secret_data)

        for cloud_service in cloud_services:
            total_resources.append(
                make_response(
                    cloud_service=cloud_service,
                    match_keys=[["name", "reference.resource_id", "account", "provider"]],
                    resource_type="inventory.CloudService",
                )
            )

        return total_resources