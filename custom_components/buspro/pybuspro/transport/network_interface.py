from .udp_client import UDPClient
from ..helpers.telegram_helper import TelegramHelper
# from ..devices.control import Control


class NetworkInterface:
    def __init__(self, buspro, gateway_address_send_receive):
        self.buspro = buspro
        self.gateway_address_send_receive = gateway_address_send_receive
        self.udp_client = None
        self.callback = None
        self._init_udp_client()
        self._th = TelegramHelper()

    def _init_udp_client(self):
        self.udp_client = UDPClient(self.buspro, self.gateway_address_send_receive, self._udp_request_received)

    def _udp_request_received(self, data, address):
        if self.callback is not None:
            telegram = self._th.build_telegram_from_udp_data(data, address)
            self.callback(telegram)

    async def _send_message(self, message):
        await self.udp_client.send_message(message)

    """
    public methods
    """
    def register_callback(self, callback):
        self.callback = callback

    async def start(self):
        await self.udp_client.start()

    async def stop(self):
        if self.udp_client is not None:
            await self.udp_client.stop()
            self.udp_client = None

    async def send_telegram(self, telegram):
        message = self._th.build_send_buffer(telegram)

        gateway_address_send, _ = self.gateway_address_send_receive
        self.buspro.logger.debug(self._th.build_telegram_from_udp_data(message, gateway_address_send))

        await self.udp_client.send_message(message)
