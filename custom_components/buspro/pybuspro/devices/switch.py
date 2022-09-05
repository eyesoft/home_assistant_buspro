from .control import _SingleChannelControl
from .device import Device
from ..helpers.enums import *
from ..helpers.generics import Generics


class Switch(Device):
    def __init__(self, buspro, device_address, channel_number, name="", delay_read_current_state_seconds=0):
        super().__init__(buspro, device_address, name)
        # device_address = (subnet_id, device_id, channel_number)

        self._buspro = buspro
        self._device_address = device_address
        self._channel = channel_number
        self._brightness = 0
        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_status_of_channels(run_from_init=True)

    def _telegram_received_cb(self, telegram):
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            channel = telegram.payload[0]
            # success = telegram.payload[1]
            brightness = telegram.payload[2]
            if channel == self._channel:
                self._brightness = brightness
                self._call_device_updated()
        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if self._channel <= telegram.payload[0]:
                self._brightness = telegram.payload[self._channel]
                self._call_device_updated()
        elif telegram.operate_code == OperateCode.SceneControlResponse:
            self._call_read_current_status_of_channels()

    async def set_on(self):
        intensity = 100
        await self._set(intensity, 0)

    async def set_off(self):
        intensity = 0
        await self._set(intensity, 0)

    async def read_status(self):
        raise NotImplementedError

    @property
    def supports_brightness(self):
        return False

    @property
    def is_on(self):
        if self._brightness == 0:
            return False
        else:
            return True

    @property
    def device_identifier(self):
        return f"{self._device_address}-{self._channel}"

    async def _set(self, intensity, running_time_seconds):
        self._brightness = intensity

        generics = Generics()
        (minutes, seconds) = generics.calculate_minutes_seconds(running_time_seconds)

        scc = _SingleChannelControl(self._buspro)
        scc.subnet_id, scc.device_id = self._device_address
        scc.channel_number = self._channel
        scc.channel_level = intensity
        scc.running_time_minutes = minutes
        scc.running_time_seconds = seconds
        await scc.send()
