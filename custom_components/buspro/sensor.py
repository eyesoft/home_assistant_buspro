"""
This component provides sensor support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, 
    CONF_DEVICES, 
    CONF_ADDRESS, 
    CONF_TYPE, 
    CONF_UNIT_OF_MEASUREMENT,
    ILLUMINANCE, 
    TEMPERATURE, 
    CONF_DEVICE_CLASS, 
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity

from ..buspro import DATA_BUSPRO

DEFAULT_CONF_UNIT_OF_MEASUREMENT = ""
DEFAULT_CONF_DEVICE_CLASS = "None"
DEFAULT_CONF_SCAN_INTERVAL = 0
DEFAULT_CONF_OFFSET = 0
CONF_DEVICE = "device"
CONF_OFFSET = "offset"
SCAN_INTERVAL = timedelta(minutes=2)

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    ILLUMINANCE,
    TEMPERATURE,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ADDRESS): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_TYPE): vol.In(SENSOR_TYPES),
                vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_CONF_UNIT_OF_MEASUREMENT): cv.string,
                vol.Optional(CONF_DEVICE_CLASS, default=DEFAULT_CONF_DEVICE_CLASS): cv.string,
                vol.Optional(CONF_DEVICE, default=None): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_CONF_SCAN_INTERVAL): cv.string,
                vol.Optional(CONF_OFFSET, default=DEFAULT_CONF_OFFSET): cv.string,
            })
        ])
})


# noinspection PyUnusedLocal
async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro switch devices."""
    # noinspection PyUnresolvedReferences
    from .pybuspro.devices import Sensor

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []

    for device_config in config[CONF_DEVICES]:
        address = device_config[CONF_ADDRESS]
        name = device_config[CONF_NAME]
        sensor_type = device_config[CONF_TYPE]
        device = device_config[CONF_DEVICE]
        offset = device_config[CONF_OFFSET]
        
        scan_interval = device_config[CONF_SCAN_INTERVAL]
        interval = 0
        if scan_interval is not None:
            interval = int(scan_interval)
            
        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))

        _LOGGER.debug("Adding sensor '{}' with address {}, sensor type '{}'".format(
            name, device_address, sensor_type))

        sensor = Sensor(hdl, device_address, device=device, name=name)

        devices.append(BusproSensor(hass, sensor, sensor_type, interval, offset))

    async_add_entites(devices)


# noinspection PyAbstractClass
class BusproSensor(Entity):
    """Representation of a Buspro switch."""

    def __init__(self, hass, device, sensor_type, scan_interval, offset):
        self._hass = hass
        self._device = device
        self._sensor_type = sensor_type
        self.async_register_callbacks()
        self._offset = offset
        self._temperature = None
        self._brightness = None

        self._should_poll = False
        if scan_interval > 0:
            self._should_poll = True

    @callback
    def async_register_callbacks(self):
        """Register callbacks to update hass after device was changed."""

        # noinspection PyUnusedLocal
        async def after_update_callback(device):
            """Call after device was updated."""
            if self._hass is not None:
                self._temperature = self._device.temperature
                self._brightness = self._device.brightness
                self.async_write_ha_state()

        self._device.register_device_updated_cb(after_update_callback)

    @property
    def should_poll(self):
        """No polling needed within Buspro unless explicitly set."""
        return self._should_poll

    async def async_update(self):
        await self._device.read_sensor_status()

    @property
    def name(self):
        """Return the display name of this light."""
        return self._device.name

    @property
    def available(self):
        """Return True if entity is available."""
        connected = self._hass.data[DATA_BUSPRO].connected

        if self._sensor_type == TEMPERATURE:
            return connected and self._current_temperature is not None

        if self._sensor_type == ILLUMINANCE:
            return connected and self._brightness is not None

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._sensor_type == TEMPERATURE:
            return self._current_temperature

        if self._sensor_type == ILLUMINANCE:
            return self._brightness

    @property
    def _current_temperature(self):
        if self._temperature is None:
            return None

        temperature = self._temperature
        if self._offset is not None and temperature != 0:
            temperature = temperature + int(self._offset)

        return temperature

    @property
    def device_class(self):
        """Return the class of this sensor."""
        if self._sensor_type == TEMPERATURE:
            return "temperature"
        if self._sensor_type == ILLUMINANCE:
            return "illuminance"
        return None

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        if self._sensor_type == TEMPERATURE:
            return "°C"
        if self._sensor_type == ILLUMINANCE:
            return "lux"
        return ""

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = {}
        attributes['state_class'] = "measurement"
        return attributes

    @property
    def unique_id(self):
        """Return the unique id."""
        return f"{self._device.device_identifier}-{self._sensor_type}"
