from .device import Device
# from ..helpers.enums import *
from ..devices.control import _GenericControl


class Generic(Device):
    def __init__(self, buspro, device_address, payload, operate_code, name=""):
        super().__init__(buspro, device_address, name)
        # device_address = (subnet_id, device_id, area_number, scene_number)

        self._buspro = buspro
        self._device_address = device_address
        self._payload = payload
        self._operate_code = operate_code
        # self.register_telegram_received_cb(self._telegram_received_cb)
        # self._call_read_current_status_of_channels(run_from_init=True)

    def _telegram_received_cb(self, telegram):
        """
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            channel, success, brightness = tuple(telegram.payload)
            if channel == self._channel:
                self._brightness = brightness
                self.call_device_updated()
        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if self._channel <= telegram.payload[0]:
                self._brightness = telegram.payload[self._channel]
                self.call_device_updated()
        """

        # Litt usikker på dette kallet
        # if telegram.operate_code == OperateCode.SceneControlResponse:
        #     self._call_read_current_status_of_channels()

    async def run(self):
        generic_control = _GenericControl(self._buspro)
        generic_control.subnet_id, generic_control.device_id = self._device_address
        generic_control.payload = self._payload
        generic_control.operate_code = self._operate_code
        await generic_control.send()
