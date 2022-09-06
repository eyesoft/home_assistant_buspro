pybuspro - A Buspro Library Written in Python
====================================================

Example
-------

```python
"""Example for switching a light on and off."""
import asyncio

from pybuspro.buspro import Buspro
from pybuspro.devices.light import Light

GATEWAY_ADDRESS_SEND_RECEIVE = (('127.0.0.1', 6000), ('', 6000))


def callback_all_messages(telegram):
    print(telegram)
    pass
    
    
async def main():
    """Connect to Buspro bus, switch on light, wait 2 seconds and switch of off again."""
    buspro = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE)
    # buspro.register_telegram_received_cb_2(callback_all_messages)
    await buspro.start()
    
    light = Light(buspro, device_address=(1, 100), channel_number=9, name="name of light")
    await light.set_on()
    await asyncio.sleep(2)
    await light.set_off()
    
    # await buspro.disconnect()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()

```
