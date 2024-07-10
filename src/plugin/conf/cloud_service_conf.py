from enum import Enum

class AUTH_TYPE(Enum):
    TOKEN = "nhncloud-access-key"
    APP_KEY = "nhncloud-app-key"

ASSET_URL="https://raw.githubusercontent.com/cloudforet-io/static-assets/master/providers/nhncloud"
PROVIDER_NAME="nhncloud"