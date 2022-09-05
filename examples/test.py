

class NetworkInterface:
    @staticmethod
    def send_control(control):

        if control is None:
            print("NOTSET")
        elif type(control) == Control.SingleChannelControl:
            print("JA SCC")
        elif type(control) == Control.SceneControl:
            print("JA SC")
        else:
            print("<UNKNOWN>")


class Control:
    class SingleChannelControl:
        def __init__(self):
            # self.address = None     # [1,71] # list(map(int, "1.74".split(".")))
            self.subnet_id = None
            self.device_id = None
            self.channel_number = None
            self.channel_level = None
            self.running_time_minutes = None
            self.running_time_seconds = None

    class SceneControl:
        def __init__(self):
            self.subnet_id = None
            self.device_id = None
            self.area_number = None
            self.scene_number = None


"""
class Action:
    def __init__(self, control):
        self._control = control

    @property
    def telegram(self):
        if self._control is None:
            return "NOTSET"
        elif type(self._control) == Control.SingleChannelControl:
            return "JA SCC"
        elif type(self._control) == Control.SceneControl:
            return "JA SC"
        else:
            return "<UNKNOWN>"
"""


def test():
    network_interface = NetworkInterface()

    scc = Control.SceneControl()
    scc.subnet_id = 1
    scc.device_id = 74

    network_interface.send_control(scc)


test()
