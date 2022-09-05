import traceback
from struct import *

from .enums import DeviceType
from .generics import Generics
from ..core.telegram import Telegram
from ..devices.control import *


class TelegramHelper:

    def build_telegram_from_udp_data(self, data, address):
        if not data:
            print("build_telegram_from_udp_data: not data")
            return None

        try:
            index_length_of_data_package = 16
            index_original_subnet_id = 17
            index_original_device_id = 18
            index_original_device_type = 19
            index_operate_code = 21
            index_target_subnet_id = 23
            index_target_device_id = 24
            index_content = 25
            length_of_data_package = data[index_length_of_data_package]

            source_device_id = data[index_original_device_id]
            content_length = length_of_data_package - 1 - 1 - 1 - 2 - 2 - 1 - 1 - 1 - 1
            source_subnet_id = data[index_original_subnet_id]
            source_device_type_hex = data[index_original_device_type:index_original_device_type + 2]
            operate_code_hex = data[index_operate_code:index_operate_code + 2]
            target_subnet_id = data[index_target_subnet_id]
            target_device_id = data[index_target_device_id]
            content = data[index_content:index_content + content_length]
            crc = data[-2:]

            generics = Generics()

            telegram = Telegram()
            telegram.source_device_type = generics.get_enum_value(DeviceType, source_device_type_hex)
            telegram.udp_data = data
            telegram.source_address = (source_subnet_id, source_device_id)
            telegram.operate_code = generics.get_enum_value(OperateCode, operate_code_hex)
            telegram.target_address = (target_subnet_id, target_device_id)
            telegram.udp_address = address
            telegram.payload = generics.hex_to_integer_list(content)
            telegram.crc = crc

            crc_check_pass = self._check_crc(telegram)
            if not crc_check_pass:
                print("crc check failed")
                return None

            return telegram
        except Exception as e:
            print("error building telegram: {}".format(traceback.format_exc()))
            return None

    @staticmethod
    def replace_none_values(telegram: Telegram):
        if telegram is None:
            return None
        if telegram.payload is None:
            telegram.payload = []
        if telegram.source_address is None:
            telegram.source_address = [200, 200]
        if telegram.source_device_type is None:
            telegram.source_device_type = DeviceType.PyBusPro
        return telegram

    # noinspection SpellCheckingInspection
    def build_send_buffer(self, telegram: Telegram):
        send_buf = bytearray([192, 168, 1, 15])
        # noinspection SpellCheckingInspection
        send_buf.extend('HDLMIRACLE'.encode())
        send_buf.append(0xAA)
        send_buf.append(0xAA)

        if telegram is None:
            return None

        if telegram.payload is None:
            telegram.payload = []

        length_of_data_package = 11 + len(telegram.payload)
        send_buf.append(length_of_data_package)

        if telegram.source_address is not None:
            sender_subnet_id, sender_device_id = telegram.source_address
        else:
            sender_subnet_id = 200
            sender_device_id = 200

        send_buf.append(sender_subnet_id)
        send_buf.append(sender_device_id)

        if telegram.source_device_type is not None:
            source_device_type_hex = telegram.source_device_type.value
            send_buf.append(source_device_type_hex[0])
            send_buf.append(source_device_type_hex[1])
        else:
            send_buf.append(0)
            send_buf.append(0)

        # if telegram.source_device_type_hex is not None:
        #    send_buf.append(telegram.source_device_type_hex[0])
        #    send_buf.append(telegram.source_device_type_hex[1])
        # else:
        #     send_buf.append(0)
        #    send_buf.append(0)
        #    # send_buf.append(b'\x00\x00')

        operate_code_hex = telegram.operate_code.value
        send_buf.append(operate_code_hex[0])
        send_buf.append(operate_code_hex[1])

        target_subnet_id, target_device_id = telegram.target_address
        send_buf.append(target_subnet_id)
        send_buf.append(target_device_id)

        for byte in telegram.payload:
            send_buf.append(byte)

        # crc_buf_length = length_of_data_package - 2
        # crc_buf = send_buf[-crc_buf_length:]
        # crc_buf_as_bytes = bytes(crc_buf)
        # crc = self._crc16(crc_buf_as_bytes)
        # hex_byte_array = pack(">H", crc)
        # send_buf.append(hex_byte_array[0])
        # send_buf.append(hex_byte_array[1])

        crc_0, crc_1 = self._calculate_crc(length_of_data_package, send_buf)
        send_buf.append(crc_0)
        send_buf.append(crc_1)

        return send_buf

    def _calculate_crc(self, length_of_data_package, send_buf):
        crc_buf_length = length_of_data_package - 2
        crc_buf = send_buf[-crc_buf_length:]
        crc_buf_as_bytes = bytes(crc_buf)
        crc = self._crc16(crc_buf_as_bytes)

        return pack(">H", crc)

    def _calculate_crc_from_telegram(self, telegram):
        length_of_data_package = 11 + len(telegram.payload)
        crc_buf_length = length_of_data_package - 2
        send_buf = telegram.udp_data[:-2]
        crc_buf = send_buf[-crc_buf_length:]
        crc_buf_as_bytes = bytes(crc_buf)
        crc = self._crc16(crc_buf_as_bytes)
        
        return pack(">H", crc)

    def _check_crc(self, telegram):
        # crc = data[-2:]
        calculated_crc = self._calculate_crc_from_telegram(telegram)
        if calculated_crc == telegram.crc:
            return True
        return False

    @staticmethod
    def _crc16(data: bytes):
        xor_in = 0x0000  # initial value
        xor_out = 0x0000  # final XOR value
        poly = 0x1021  # generator polinom (normal form)
    
        reg = xor_in
        for octet in data:
            # reflect in
            for i in range(8):
                topbit = reg & 0x8000
                if octet & (0x80 >> i):
                    topbit ^= 0x8000
                reg <<= 1
                if topbit:
                    reg ^= poly
            reg &= 0xFFFF
            # reflect out
        return reg ^ xor_out
