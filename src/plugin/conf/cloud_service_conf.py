from enum import Enum

class AUTH_TYPE(Enum):
    TOKEN = "nhncloud-access-key"
    APP_KEY = "nhncloud-app-key"

ASSET_URL="https://raw.githubusercontent.com/cloudforet-io/static-assets/master/providers/nhncloud"
PROVIDER_NAME="nhncloud"
class REGION(Enum):
    KR1 = "Korea(Pangyo)"
    KR2 = "Korea(Pyeongchon)"
    JP1 = "Japan(Tokyo)"
    US1 = "US(California)"

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]