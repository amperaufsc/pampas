from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ThrottleLimits:
    """Throttle limits for the hardware controller."""

    min: float
    max: float


@dataclass
class SteeringLimits:
    """Steering limits for the hardware controller."""

    min: float
    max: float


class HardwareInterface(ABC):
    """Abstract interface for interacting with the steering and throttle actuators."""

    def __init__(
        self, throttle_limits: ThrottleLimits, steering_limits: SteeringLimits
    ) -> None:

        super().__init__()
        self._throttle_limits = throttle_limits
        self._steering_limits = steering_limits

        self._throttle: float = 0.0  # Bound to [0.0, 1.0]
        self._steering: float = 0.0  # Bound to [-1.0, 1.0]

    @property
    def throttle(self) -> float:
        """Returns the last throttle reference value given to the controller."""
        return self._throttle

    @abstractmethod
    def set_throttle(self, value: float):
        """Commands the Electrical Control Unit (ECU) to set the motor throttle value to the given value."""

        if not isinstance(value, float):
            raise TypeError(
                f"Steering reference value must be a float, got {type(value)}"
            )
        if not (value >= 0.0 and value <= 1.0):
            raise ValueError(
                f"Steering reference value must be between -1.0 and 1.0, got {value}"
            )

    @property
    def steering(self) -> float:
        """Returns the last steering reference value given to the controller."""
        return self._steering

    @abstractmethod
    def steer(self, value: float) -> None:
        """Commands the steering actuator to steer to the given reference value."""

        if not isinstance(value, float):
            raise TypeError(
                f"Steering reference value must be a float, got {type(value)}"
            )
        if not (value >= -1.0 and value <= 1.0):
            raise ValueError(
                f"Steering reference value must be between -1.0 and 1.0, got {value}"
            )

    @abstractmethod
    def steering_position(self) -> float:
        """Returns the normalized [-1, 1] steering value read by the steering sensor."""

    @abstractmethod
    def shutdown(self) -> None:
        """Turns off the hardware controller, setting the steering and throttle reference values to 0 and properly shutting down the underlying hardware."""
