import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_USERNAME, CONF_IP_ADDRESS

from homeassistant.helpers.discovery import async_load_platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "router_query"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_IP_ADDRESS): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the Router Query component."""
    conf = config[DOMAIN]
    router_ip = conf[CONF_IP_ADDRESS]
    username = conf[CONF_USERNAME]
    password = conf[CONF_PASSWORD]

    # Set up the Router Query platform
    hass.async_create_task(
        async_load_platform(hass, "sensor", DOMAIN, {"router_ip": router_ip, "username": username, "password": password}, config)
    )

    return True
