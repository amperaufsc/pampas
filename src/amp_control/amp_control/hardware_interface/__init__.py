"""Hardware integration layers for the controlling the steering and throttle."""

from enum import Enum

from .arduino.arduino_interface import ArduinoInterface as ArduinoInterface
from .hardware_interface import HardwareInterface as HardwareInterface
from .hardware_interface import SteeringLimits, ThrottleLimits
from .jetson.jetson_interface import JetsonController as JetsonController


class HardwareInterfaceOption(Enum):
    """Enum for the different hardware interfaces available."""

    ARDUINO = 1
    JETSON = 2


def hardware_controller_factory(
    interface: HardwareInterface,
    throttle_limits: ThrottleLimits,
    steering_limits: SteeringLimits,
    *args,
    **kwargs,
) -> HardwareInterface:
    match interface:
        case HardwareInterfaceOption.ARDUINO:
            return ArduinoInterface(throttle_limits, steering_limits, *args, **kwargs)
        case HardwareInterfaceOption.JETSON:
            return JetsonController(throttle_limits, steering_limits, *args, **kwargs)
        case _:
            return ArduinoInterface(throttle_limits, steering_limits, *args, **kwargs)
