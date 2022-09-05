''' pybuspro version 1.0.0  '''

import asyncio
import logging

from .helpers.enums import *
from .transport.network_interface import NetworkInterface


# ip, port = gateway_address
# subnet_id, device_id, channel = device_address


class StateUpdater:
    def __init__(self, buspro, sleep=10):
        self.buspro = buspro
        self.run_forever = True
        self.run_task = None
        self.sleep = sleep

    async def start(self):
        self.run_task = self.buspro.loop.create_task(self.run())

    async def run(self):
        await asyncio.sleep(0)
        self.buspro.logger.info("Starting StateUpdater with {} seconds interval".format(self.sleep))

        while True:
            await asyncio.sleep(self.sleep)
            await self.buspro.sync()


class Buspro:

    def __init__(self, gateway_address_send_receive, loop_=None):
        self.loop = loop_ or asyncio.get_event_loop()
        self.state_updater = None
        self.started = False
        self.network_interface = None
        self.logger = logging.getLogger("buspro.log")
        self.telegram_logger = logging.getLogger("buspro.telegram")

        self.callback_all_messages = None
        self._telegram_received_cbs = []

        self.gateway_address_send_receive = gateway_address_send_receive

    def __del__(self):
        if self.started:
            try:
                task = self.loop.create_task(self.stop())
                self.loop.run_until_complete(task)
            except RuntimeError as exp:
                self.logger.warning("Could not close loop, reason: {}".format(exp))

    # noinspection PyUnusedLocal
    async def start(self, state_updater=False):  # , daemon_mode=False):
        self.network_interface = NetworkInterface(self, self.gateway_address_send_receive)
        self.network_interface.register_callback(self._callback_all_messages)
        await self.network_interface.start()

        if state_updater:
            self.state_updater = StateUpdater(self)
            await self.state_updater.start()

        '''
        if daemon_mode:
            await self._loop_until_sigint()
        '''

        self.started = True

        # await asyncio.sleep(5)
        # await self.network_interface.send_message(b'\0x01')

    async def stop(self):
        await self._stop_network_interface()
        self.started = False

    def _callback_all_messages(self, telegram):
        self.telegram_logger.debug(telegram)

        if self.callback_all_messages is not None:
            self.callback_all_messages(telegram)

        for telegram_received_cb in self._telegram_received_cbs:
            device_address = telegram_received_cb['device_address']

            # Sender callback kun for oppgitt kanal
            if device_address == telegram.target_address or device_address == telegram.source_address:
                if telegram.operate_code is not OperateCode.TIME_IF_FROM_LOGIC_OR_SECURITY:
                    postfix = telegram_received_cb['postfix']
                    if postfix is not None:
                        telegram_received_cb['callback'](telegram, postfix)
                    else:
                        telegram_received_cb['callback'](telegram)

    async def _stop_network_interface(self):
        if self.network_interface is not None:
            await self.network_interface.stop()
            self.network_interface = None

    def register_telegram_received_all_messages_cb(self, telegram_received_cb):
        self.callback_all_messages = telegram_received_cb

    def register_telegram_received_device_cb(self, telegram_received_cb, device_address, postfix=None):
        self._telegram_received_cbs.append({
            'callback': telegram_received_cb,
            'device_address': device_address,
            'postfix': postfix})

    def unregister_telegram_received_device_cb(self, telegram_received_cb, device_address, postfix=None):
        self._telegram_received_cbs.remove({
            'callback': telegram_received_cb,
            'device_address': device_address,
            'postfix': postfix})

    @staticmethod
    async def sync():
        # await self.callback("LOG: Sync() triggered from StateUpdater")
        # print("LOG: Sync() triggered from StateUpdater")
        raise NotImplementedError
