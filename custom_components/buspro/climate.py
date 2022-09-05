"""
This component provides sensor support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging
from typing import Optional, List

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.climate import (
    PLATFORM_SCHEMA, 
    ClimateEntity,
)
from homeassistant.components.climate.const import (
    SUPPORT_PRESET_MODE, 
    SUPPORT_TARGET_TEMPERATURE,
    HVAC_MODE_HEAT, 
    HVAC_MODE_OFF,
    CURRENT_HVAC_IDLE,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_OFF,
)
from homeassistant.const import (
    CONF_NAME, 
    CONF_DEVICES, 
    CONF_ADDRESS, 
    TEMP_CELSIUS, 
    ATTR_TEMPERATURE,
)
from homeassistant.core import callback

# from homeassistant.helpers.entity import Entity
from ..buspro import DATA_BUSPRO
# noinspection PyUnresolvedReferences
from .pybuspro.devices.climate import ControlFloorHeatingStatus
# noinspection PyUnresolvedReferences
from .pybuspro.helpers.enums import OnOffStatus

_LOGGER = logging.getLogger(__name__)

CONF_SUPPORTS_OPERATION_MODE = "supports_operation_mode"
CONF_RELAY_ADDRESS = "relay_address"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ADDRESS): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Optional(CONF_SUPPORTS_OPERATION_MODE, default=True): cv.boolean,
                vol.Optional(CONF_RELAY_ADDRESS, default=''): cv.string,
            })
        ])
})


# noinspection PyUnusedLocal
async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro switch devices."""
    # noinspection PyUnresolvedReferences
    from .pybuspro.devices import Climate
    from .pybuspro.devices import Sensor

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []

    for device_config in config[CONF_DEVICES]:
        address = device_config[CONF_ADDRESS]
        name = device_config[CONF_NAME]
        supports_operation_mode = device_config[CONF_SUPPORTS_OPERATION_MODE]

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))

        _LOGGER.debug("Adding climate '{}' with address {}".format(name, device_address))

        climate = Climate(hdl, device_address, name)

        relay_sensor = None
        relay_address = device_config[CONF_RELAY_ADDRESS]
        if relay_address: 
            relay_address2 = relay_address.split('.')
            relay_device_address = (int(relay_address2[0]), int(relay_address2[1]))
            relay_channel_number = int(relay_address2[2])
            relay_sensor = Sensor(hdl, relay_device_address, channel_number=relay_channel_number)

        devices.append(BusproClimate(hass, climate, supports_operation_mode, relay_sensor))

    async_add_entites(devices)


# noinspection PyAbstractClass
class BusproClimate(ClimateEntity):
    """Representation of a Buspro switch."""

    def __init__(self, hass, device, supports_operation_mode, relay_sensor):
        self._hass = hass
        self._device = device
        self._target_temperature = self._device.target_temperature
        self._is_on = self._device.is_on
        self._supports_operation_mode = supports_operation_mode

        self._relay_sensor = relay_sensor
        self._relay_sensor_is_on = None
        if (self._relay_sensor is not None):
            self._relay_sensor_is_on = self._relay_sensor.single_channel_is_on

        self.async_register_callbacks()

    @callback
    def async_register_callbacks(self):
        """Register callbacks to update hass after device was changed."""

        # noinspection PyUnusedLocal
        async def after_update_callback(device):
            """Call after device was updated."""
            self._target_temperature = device.target_temperature
            self._is_on = device.is_on
            if (self._hass is not None):
                await self.async_update_ha_state()

        async def after_relay_sensor_update_callback(device):
            """Call after device was updated."""
            self._relay_sensor_is_on = device.single_channel_is_on
            await self.async_update_ha_state()

        self._device.register_device_updated_cb(after_update_callback)
        
        if self._relay_sensor is not None:
            self._relay_sensor.register_device_updated_cb(after_relay_sensor_update_callback)

    @property
    def should_poll(self):
        """No polling needed within Buspro."""
        return False

    @property
    def name(self):
        """Return the display name of this light."""
        return self._device.name

    @property
    def available(self):
        """Return True if entity is available."""
        return self._hass.data[DATA_BUSPRO].connected

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._device.temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        target_temperature = self._target_temperature
        if target_temperature is None:
            target_temperature = self._device.target_temperature

        return target_temperature

    @property
    def supported_features(self):
        """Return the list of supported features."""
        support = SUPPORT_TARGET_TEMPERATURE
        if self._supports_operation_mode:
            support |= SUPPORT_PRESET_MODE
        return support

    @property
    def preset_mode(self) -> Optional[str]:
        """Return the current preset mode, e.g., home, away, temp.
        Requires SUPPORT_PRESET_MODE.
        """
        return None

    @property
    def preset_modes(self) -> Optional[List[str]]:
        """Return a list of available preset modes.
        Requires SUPPORT_PRESET_MODE.
        """
        return None

    @property
    def hvac_action(self) -> Optional[str]:
        """Return current action ie. heating, idle, off."""
        if self._device.is_on:
            
            if self._relay_sensor_is_on is None:
                return CURRENT_HVAC_HEAT
            else:
                if self._relay_sensor_is_on:
                    return CURRENT_HVAC_HEAT
                else:
                    return CURRENT_HVAC_IDLE
        else:
            return CURRENT_HVAC_OFF

    @property
    def hvac_mode(self) -> Optional[str]:
        """Return current operation ie. heat, cool, idle."""
        if self._device.is_on:
            return HVAC_MODE_HEAT
        else:
            return HVAC_MODE_OFF

    @property
    def hvac_modes(self) -> Optional[List[str]]:
        """Return the list of available operation modes."""
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF]

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set operation mode."""
        if hvac_mode == HVAC_MODE_OFF:
            self._is_on = False
            climate_control = ControlFloorHeatingStatus()
            climate_control.status = OnOffStatus.OFF.value
            await self._device.control_heating_status(climate_control)
            await self.async_update_ha_state()
        elif hvac_mode == HVAC_MODE_HEAT:
            self._is_on = True
            climate_control = ControlFloorHeatingStatus()
            climate_control.status = OnOffStatus.ON.value
            await self._device.control_heating_status(climate_control)
            await self.async_update_ha_state()
        else:
            _LOGGER.error("Unrecognized operation mode: %s", operation_mode)
            return

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 1

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._device.device_identifier

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        self._target_temperature = temperature
        climate_control = ControlFloorHeatingStatus()
        climate_control.normal_temperature = int(temperature)
        await self._device.control_heating_status(climate_control)

        await self.async_update_ha_state()
