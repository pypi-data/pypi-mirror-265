"""SmartCocoon constants."""

from enum import Enum

# API Data
API_URL = "https://app.mysmartcocoon.com/api/"
API_AUTH_URL = API_URL + "auth/sign_in"
API_FANS_URL = API_URL + "fans/"
API_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "SmartCocoon/1 CFNetwork/1312 Darwin/21.0.0",
}

# Default fan speed is 38% in the SmartCocoon app
# but 33% works better for HomeAssistant
DEFAULT_FAN_POWER_PCT = 33

# MQTT Data
MQTT_BROKER = "nlb-production-04b5ef4727e9be7d.elb.us-east-2.amazonaws.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 600

DEFAULT_TIMEOUT: int = 30


class EntityType(Enum):
    """Class to define entity types"""

    # SmartCocoon entity types

    LOCATIONS = "client_systems"
    THERMOSTATS = "thermostats"
    ROOMS = "rooms"
    FANS = "fans"


class FanMode(Enum):
    """Fan mode."""

    ECO = "eco"
    OFF = "always_off"
    ON = "always_on"
    AUTO = "auto"


class FanState(Enum):
    """Fan State."""

    FAN_OFF = "false"
    FAN_ON = "true"
