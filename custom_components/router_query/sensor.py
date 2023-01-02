import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_RESOURCES,
    CONF_UNIT_OF_MEASUREMENT,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_TYPE = "device_type"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_RESOURCES, default=[]): vol.All(
            cv.ensure_list, [cv.string]
        ),
        vol.Required(CONF_DEVICE_TYPE): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Router Query sensor platform."""
    name = config.get(CONF_NAME)
    device_type = config.get(CONF_DEVICE_TYPE)
    resources = config.get(CONF_RESOURCES)
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)

    sensors = []
    for resource in resources:
        sensors.append(RouterQuerySensor(hass, name, device_type, resource, unit))

    add_entities(sensors)


class RouterQuerySensor(Entity):
    """Representation of a Router Query sensor."""

    def __init__(self, hass, name, device_type, resource, unit):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._device_type = device_type
        self._resource = resource
        self._unit_of_measurement = unit
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        attrs = {}
        attrs["device_type"] = self._device_type
        return attrs

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return self._unit_of_measurement

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        # Call the service to query the router for the desired resource
        service_data = {"device_type": self._device_type, "resource": self._resource}
        self._hass.services.call("router_query", "query", service_data)

        # Update the sensor state with the result of the query
        self._state = self._hass.data["router_query"]["result"]
