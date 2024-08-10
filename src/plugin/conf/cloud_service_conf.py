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

REGION_INFORMATIONS = {
    "kr1": {
        "name": "Korea(Pangyo)",
        "tags": {
            "latitude": "37.394726",
            "longitude": "127.111209",
            "continent": "asia_pacific",
        },
        "region_code": "kr1",
    },
    "kr2": {
        "name": "Korea(Pyeongchon)",
        "tags": {
            "latitude": "37.394250",
            "longitude": "126.963778",
            "continent": "asia_pacific",
        },
        "region_code": "kr2",
    },
    "jp1": {
        "name": "Japan(Tokyo)",
        "tags": {
            "latitude": "35.680790",
            "longitude": "139.767733",
            "continent": "asia_pacific",
        },
        "region_code": "jp1",
    },
    "us1": {
        "name": "US(California)",
        "tags": {
            "latitude": "34.052220",
            "longitude": "-118.243610",
            "continent": "north_america",
        },
        "region_code": "us1",
    },
}