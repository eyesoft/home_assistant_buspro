import asyncio
import random

from pybuspro.buspro import Buspro
from pybuspro.devices.climate import Climate, ControlFloorHeatingStatus
# noinspection PyProtectedMember
from pybuspro.devices.control import _ReadStatusOfChannels
from pybuspro.devices.light import Light
from pybuspro.devices.scene import Scene
from pybuspro.devices.sensor import Sensor
from pybuspro.devices.switch import Switch
from pybuspro.devices.universal_switch import UniversalSwitch
from pybuspro.helpers.enums import *

# ip, port = gateway_address
# subnet_id, device_id, channel = device_address

# GATEWAY_ADDRESS_SEND_RECEIVE = (('192.168.34.123', 6000), ('192.168.34.121', 6000))
GATEWAY_ADDRESS_SEND_RECEIVE = (('192.168.1.15', 6000), ('', 6000))
# GATEWAY_ADDRESS_SEND_RECEIVE = (('10.120.1.66', 6000), ('10.120.1.66', 6000))
# GATEWAY_ADDRESS_SEND_RECEIVE = (('127.0.0.1', 6000), ('127.0.0.1', 6000))


def callback_received_for_all_messages(telegram):
    print(f'Callback all messages: {telegram}')


def callback_received_for_all_messages_to_file(telegram):
    print(f'Callback all messages: {telegram}')
    with open('telegrams.txt', 'a') as the_file:
        the_file.write('{}\n\n'.format(str(telegram)))


async def main__send_and_receive_random_messages():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    async def send_random_message(hdl_):
        messages = [
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\r\x012\x014\x00\x02\x01H\x01\t\x8d\x1b',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01(\x014\x001\x01J\x04\x00\x00\x03\xc4c',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x012\x014\x001\x01\x83\x05d\x00\x00\t\xdb',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0e\x01J\x02`\x002\xff\xff\x04\xf8\x00\x96\xb3',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01H\x02`\x00\x03\xff\xff\x01\t\x06\x05\xc6g',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x10\x01\x83\x00\x11\x002\xff\xff\x05\xf8d\x06\x10)(',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x01d\x04S\xdaD\xff\xff\x12\t\x05\x11\x1c\x00^\x05',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x82\x00\x11\xef\xff\xff\xff\x01\xfe\x06\x00u8',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x01)\x014\xe3\xe5\xff\xff\x01\x1f\x00\x00\xf8A\xac4',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x011\x014\xe3\xe5\xff\xff\x01\x1f\x00\x00\xf8A\xb1\xda',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x01n\x0b\xe9\xdaD\xff\xff\x12\x07\x13\x11\x18\x00\x87\xf8',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x01\x83\x00\x11\xef\xff\xff\xff\x03\xfe\xfe\xff\x06\x10\\\n',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x14\x01(\x014\x16G\xff\xff2\x00\x19\x00\x00\x00\x00\x00\x00\xfbC',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x14\x011\x014\x16G\xff\xff3\x00\x00\x00\x00\x00\x00\x00\x00\x96|',
            b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x14\x01)\x014\x16G\xff\xff3\x00\x00\x00\x00\x00\x00\x00\x00\xa4\xf3',
        ]

        while True:
            await hdl_.network_interface.send_message(random.choice(messages))
            await asyncio.sleep(2)

    await send_random_message(hdl)


async def main__turn_light_on_off():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    def callback_received_for_light(telegram):
        print(f'Callback light: {telegram}')

    # Lys kino
    light = Light(hdl, (1, 74), 1, "kino")
    light.register_telegram_received_cb(callback_received_for_light)

    await light.set_on(3)
    print("{} {}".format(light.current_brightness, light.is_on))

    await asyncio.sleep(5)
    await light.set_off()
    print("{} {}".format(light.current_brightness, light.is_on))

    await asyncio.sleep(5)
    await light.set_brightness(20, 5)
    print("{} {}".format(light.current_brightness, light.is_on))

    await asyncio.sleep(10)
    await light.set_off()


async def main__turn_light_on_off_with_device_updated_cb():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    # hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    async def device_updated_callback(light_):
        print(f"AFTER UPDATE: {light_.current_brightness}")

    def callback_received_for_light(telegram):
        print(f'Callback light: {telegram}')

    # Lys kino
    light = Light(hdl, (1, 74), 1, "kino")
    light.register_device_updated_cb(device_updated_callback)
    light.register_telegram_received_cb(callback_received_for_light)

    await light.set_brightness(30)
    # light.read_current_state()

    await light.set_on(3)
    print(f"{light.current_brightness} {light.is_on}")


async def main__turn_switch_on_off():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    def callback_received_for_switch(telegram):
        print(f'Callback switch: {telegram}')

    # Lys kino
    switch = Switch(hdl, (1, 74), 1, "kino")
    switch.register_telegram_received_cb(callback_received_for_switch)

    await switch.set_on()
    print(f"{switch.is_on}")

    await asyncio.sleep(5)
    await switch.set_off()
    print(f"{switch.is_on}")


async def main__activate_scene():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    scene = Scene(hdl, (1, 74), (2, 5), "my_scene")
    await scene.run()


async def main__set_uv_switch():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    universal_switch = UniversalSwitch(hdl, (1, 100), 101, "UV Switch")
    # await universal_switch.set_on()
    print("==>{}".format(universal_switch.is_on))


async def main__read_status():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    read_status_of_channels = _ReadStatusOfChannels(hdl)
    read_status_of_channels.subnet_id, read_status_of_channels.device_id = (1, 72)
    await read_status_of_channels.send()

    # await hdl.network_interface.send_control(read_status_of_channels)




async def main__read_sensor_status():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    # hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    '''
    def callback_received_for_sensor_status(telegram):
        print(f'==> 1: {datetime.datetime.now()} Callback telegram: {telegram}')
    '''

    async def callback_received_for_sensor_updated(device):
        # print(f'==> 2: Callback sonic: {device._sonic}')

        current_temperature = device._current_temperature - 20
        print(f'==> 2: Callback temperature: {current_temperature}')
        print(f'==> 2: Callback motion sensor: {device._motion_sensor}')

        # if device._sonic == 1 or device._motion_sensor == 1:
        #     print(f'==> 2: Bevegelse')
        # if device._sonic == 0 and device._motion_sensor == 0:
        #     print(f'==> 2: Ingen bevegelse')

        if device._motion_sensor == 1:
            print(f'==> 2: Bevegelse')
        if device._motion_sensor == 0:
            print(f'==> 2: Ingen bevegelse')

    sensor = Sensor(hdl, (1, 48), device='sensors_in_one')
    # sensor = Sensor(hdl, (1, 100), universal_switch_number=101)
    # sensor.register_telegram_received_cb(callback_received_for_sensor_status)
    sensor.register_device_updated_cb(callback_received_for_sensor_updated)

    print("START")
    # await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    # await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    # await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    # await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    # await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    # await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    # await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    # await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    # await sensor.read_sensor_status()
    # await asyncio.sleep(3)
    await sensor.read_sensor_status()
    # await asyncio.sleep(1)
    print("KJØRT")
    # print(f"{sensor.temperature}, {sensor.brightness}, {sensor.dry_contact_1_is_on}, {sensor.dry_contact_2_is_on}, "
    #       f"{sensor.movement}, '{sensor.name}', '{sensor.universal_switch_is_on}'")
    # await asyncio.sleep(3)
    # print(sensor.temperature)





async def main__climate():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    climate = Climate(hdl, (1, 11))
    await climate.read_heating_status()
    await asyncio.sleep(3)
    print(f"{climate.is_on}")

    # climate_control = ControlFloorHeatingStatus()
    # climate_control.away_temperature = 15
    # climate_control.normal_temperature = 22
    # climate_control.status = OnOffStatus.ON
    # await climate.control_heating_status(climate_control)


# noinspection PyUnusedLocal
async def main__kino():
    # taklys 1, 74, 1
    # se film scene 1, 74, 1, 1
    # høre musikk scene 1, 74, 1, 2
    # spille scene 1, 74, 1, 3
    # dlp media 1, 23

    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    light = Light(hdl, (1, 74), 1)
    # await light.set_on(0)

    scene = Scene(hdl, (1, 74), (1, 1))
    # await scene.run()

    scene = Scene(hdl, (1, 74), (1, 3))
    # await scene.run()

    # await light.set_off()

    # def heat_received(telegram):
    #     print(telegram)

    heat = Climate(hdl, (1, 23))
    # heat.register_telegram_received_cb(heat_received)
    # await heat.read_heating_status()

    # await asyncio.sleep(5)
    # print("temo kino: {}".format(heat.temperature))

    fhs = ControlFloorHeatingStatus
    # fhs.normal_temperature = 22
    fhs.status = OnOffStatus.OFF.value
    # noinspection PyTypeChecker
    await heat.control_heating_status(floor_heating_status=fhs)


async def lys_garasje():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    switch = Switch(hdl, (1, 80), 4)
    # await switch.set_on()
    await switch.set_off()


async def lys_kino():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    switch = Switch(hdl, (1, 74), 1)
    # await switch.set_on()
    await switch.set_off()


async def receive_telegrams():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    # hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages_to_file)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()




'''
async def main__run_scene():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    def callback_received_for_scene(telegram):
        print(f'Callback __scene: {telegram}')

    # Scene kino
    __scene = Scene(hdl, (1, 74, 1, 2), "kino")
    __scene.register_telegram_received_cb(callback_received_for_scene)

    await __scene.run()
'''

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(main__send_and_receive_random_messages())
    # loop.run_until_complete(main__turn_light_on_off())
    # loop.run_until_complete(main__turn_light_on_off_with_device_updated_cb())
    # loop.run_until_complete(main__turn_switch_on_off())
    # loop.run_until_complete(main__run_scene())
    # loop.run_until_complete(main__activate_scene())
    # loop.run_until_complete(main__read_status())
    # loop.run_until_complete(main__set_uv_switch())
    # loop.run_until_complete(main__read_sensor_status())
    # loop.run_until_complete(main__climate())
    # loop.run_until_complete(main__kino())
    # loop.run_until_complete(lys_garasje())
    # loop.run_until_complete(lys_kino())
    loop.run_until_complete(receive_telegrams())
    loop.run_forever()
