"""Hardware integration layers for the controlling the steering and throttle."""

from enum import Enum

from arduino.arduino_controller import ArduinoController as ArduinoController
from hardware_controller import HardwareController
from jetson.jetson_controller import JetsonController as JetsonController


class HardwareInterface(Enum):
    ARDUINO = 1
    JETSON = 2


def factory(cls, interface: HardwareInterface) -> HardwareController:
    match interface:
        case HardwareInterface.ARDUINO:
            return ArduinoController
        case HardwareInterface.JETSON:
            return JetsonController
