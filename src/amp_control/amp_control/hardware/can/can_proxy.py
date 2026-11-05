import can


class CanBusCommunicator:
    def __init__(self, channel: int, bustype, filters=None):
        self._channel = channel
        self.bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=500000)

        if filters:
            self.bus.set_filters(filters)

    def send_message(self, id, data) -> None:
        msg = can.Message(arbitration_id=id, data=data, is_extended_id=False)
        self.bus.send(msg)

    def read_message(self):
        return self.bus.recv(0.01)
