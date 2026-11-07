# import Jetson.GPIO
from amp_control.hardware.hardware_interface import (
    HardwareInterface,
    SteeringLimits,
    ThrottleLimits,
)


# TODO: Implement this according to the HardwareController interface
class JetsonController(HardwareInterface):
    """Hardware integration layer for Nvidia's Jetson."""

    def __init__(
        self,
        throtle_limits: ThrottleLimits,
        steering_limits: SteeringLimits,
        *agrs,
        **kwargs,
    ):
        super().__init__(throtle_limits, steering_limits)

        Jetson.GPIO.setmode(Jetson.GPIO.BOARD)
        self._pwm = Jetson.GPIO.PWM(kwargs["pwm"], 200)
        self._pwm.start(0)
        self._left = kwargs["left"]
        self._right = kwargs["right"]
        Jetson.GPIO.setup(self._left, Jetson.GPIO.OUT)
        Jetson.GPIO.setup(self._right, Jetson.GPIO.OUT)

    def set_throttle(self, value: float):
        raise NotImplementedError(
            "Throttle control is not implemented for JetsonController."
        )

    def steer(self, value: float) -> None:
        raise NotImplementedError(
            "Steering control is not implemented for JetsonController."
        )

        self._pwm.ChangeDutyCycle(abs(value))
        if value >= 0:
            Jetson.GPIO.output(self._left, True)
            Jetson.GPIO.output(self._right, False)
        else:
            Jetson.GPIO.output(self._left, False)
            Jetson.GPIO.output(self._right, True)

    def steering_position(self) -> float:
        raise NotImplementedError(
            "Steering position is not implemented for JetsonController."
        )

    def shutdown(self) -> None:
        Jetson.GPIO.cleanup()
