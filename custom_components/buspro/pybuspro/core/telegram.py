import json
from ..helpers.enums import DeviceType


# DTO class
class Telegram:
    def __init__(self):
        self.udp_address = None
        self.payload = None
        self.operate_code = None
        self.source_device_type = DeviceType.PyBusPro
        self.udp_data = None
        self.source_address = None
        self.target_address = None
        self.crc = None

    def __str__(self):
        """Return object as readable string."""

        return json.JSONEncoder().encode([
            {"name": "source_address", "value": self.source_address},
            {"name": "source_device_type", "value": str(self.source_device_type)},
            {"name": "target_address", "value": self.target_address},
            {"name": "operate_code", "value": str(self.operate_code)},
            {"name": "payload", "value": self.payload},
            {"name": "udp_address", "value": self.udp_address},
            {"name": "udp_data", "value": str(self.udp_data)},
            {"name": "crc", "value": str(self.crc)},
        ])

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
