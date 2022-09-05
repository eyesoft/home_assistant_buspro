from ..core.telegram import Telegram
from ..helpers.enums import OperateCode


class _Control:
    def __init__(self, buspro):
        self._buspro = buspro
        self.subnet_id = None
        self.device_id = None

    @staticmethod
    def build_telegram_from_control(control):

        if control is None:
            return None

        if type(control) == _SingleChannelControl:
            operate_code = OperateCode.SingleChannelControl
            payload = [control.channel_number, control.channel_level, control.running_time_minutes,
                       control.running_time_seconds]

        elif type(control) == _SceneControl:
            operate_code = OperateCode.SceneControl
            payload = [control.area_number, control.scene_number]

        elif type(control) == _ReadStatusOfChannels:
            operate_code = OperateCode.ReadStatusOfChannels
            payload = []

        elif type(control) == _GenericControl:
            operate_code = control.operate_code
            payload = control.payload

        elif type(control) == _UniversalSwitch:
            operate_code = OperateCode.UniversalSwitchControl
            payload = [control.switch_number, control.switch_status.value]

        elif type(control) == _ReadStatusOfUniversalSwitch:
            operate_code = OperateCode.ReadStatusOfUniversalSwitch
            payload = [control.switch_number]

        elif type(control) == _ReadSensorStatus:
            operate_code = OperateCode.ReadSensorStatus
            payload = []

        elif type(control) == _ReadSensorsInOneStatus:
            operate_code = OperateCode.ReadSensorsInOneStatus
            payload = []

        elif type(control) == _ReadFloorHeatingStatus:
            operate_code = OperateCode.ReadFloorHeatingStatus
            payload = []

        elif type(control) == _ReadDryContactStatus:
            operate_code = OperateCode.ReadDryContactStatus
            payload = [1, control.switch_number]

        elif type(control) == _ControlFloorHeatingStatus:
            operate_code = OperateCode.ControlFloorHeatingStatus
            payload = [control.temperature_type, control.status, control.mode, control.normal_temperature,
                       control.day_temperature, control.night_temperature, control.away_temperature]

        else:
            return None

        telegram = Telegram()
        telegram.target_address = (control.subnet_id, control.device_id)
        telegram.operate_code = operate_code
        telegram.payload = payload
        return telegram

    @property
    def telegram(self):
        return self.build_telegram_from_control(self)

    async def send(self):
        telegram = self.telegram

        # if telegram.target_address[1] == 100:
        #     print("==== {}".format(str(telegram)))

        await self._buspro.network_interface.send_telegram(telegram)


class _GenericControl(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.payload = None
        self.operate_code = None


class _SingleChannelControl(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.channel_number = None
        self.channel_level = None
        self.running_time_minutes = None
        self.running_time_seconds = None


class _SceneControl(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.area_number = None
        self.scene_number = None


class _ReadStatusOfChannels(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        # no more properties


class _UniversalSwitch(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.switch_number = None
        self.switch_status = None


class _ReadStatusOfUniversalSwitch(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.switch_number = None


class _ReadSensorStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        # no more properties


class _ReadSensorsInOneStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        # no more properties


class _ReadFloorHeatingStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        # no more properties


class _ControlFloorHeatingStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.temperature_type = None
        self.status = None
        self.mode = None
        self.normal_temperature = None
        self.day_temperature = None
        self.night_temperature = None
        self.away_temperature = None


class _ReadDryContactStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.switch_number = None
