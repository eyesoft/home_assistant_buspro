import aiohttp
import asyncio
import json

from collections import namedtuple
from typing import Dict, List, Tuple
import requests
import re

import logging
import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT
)

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
    
    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            try:
                return self.async_create_entry(title="Buspro", data=user_input)
                    
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",

            data_schema=vol.Schema({
            	#vol.Required(CONF_HOST, default=host): cv.string,
            	#vol.Required(CONF_PORT, default=port): cv.port
            	vol.Required(CONF_HOST): cv.string,
            	vol.Required(CONF_PORT): cv.port
            }),
            errors=errors
        )
