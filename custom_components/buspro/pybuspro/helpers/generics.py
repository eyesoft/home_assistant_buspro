from .enums import DeviceType, OperateCode


class Generics:

    @staticmethod
    def calculate_minutes_seconds(seconds):
        return divmod(seconds, 60)  # (minutes, seconds)

    @staticmethod
    def integer_list_to_hex(list_):
        hex_ = bytearray(list_)
        return hex_

    @staticmethod
    def hex_to_integer_list(hex_value):
        list_of_integer = []
        for string in hex_value:
            list_of_integer.append(string)
        return list_of_integer

    @staticmethod
    def enum_has_value(enum, value):
        return any(value == item.value for item in enum)

    def get_enum_value(self, enum, value):
        if enum == DeviceType:
            if self.enum_has_value(enum, value):
                return DeviceType(value)
            else:
                return None
        elif enum == OperateCode:
            if self.enum_has_value(enum, value):
                return OperateCode(value)
            else:
                return None
