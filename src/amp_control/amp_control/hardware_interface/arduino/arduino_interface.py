import time

import serial
from amp_control.hardware_interface import (
    HardwareInterface,
    SteeringLimits,
    ThrottleLimits,
)


class ArduinoController(HardwareInterface):
    """Hardware integration layer for Arduino."""

    def __init__(
        self,
        throttle_limits: ThrottleLimits,
        steering_limits: SteeringLimits,
        port: str = "/dev/ttyUSB0",
        baud: int = 115200,
    ):
        super().__init__(throttle_limits, steering_limits)

        self._serial = serial.Serial(port, baud, timeout=0.01)
        self._buffer = b""
        self._last_rx = None
        self._raw_sensor_value = None
        self._left_limit_triggered = False
        self._right_limit_triggered = False

    def set_throttle(self, value: float):
        super().set_throttle(value)
        raise NotImplementedError(
            "Throttle control is not implemented for ArduinoController."
        )

    def steer(self, value: float) -> None:
        super().steer(value)
        value = max(-100.0, min(100.0, float(value)))
        self._serial.write(f"S,{value:.1f}\n".encode())

    def steering_position(self) -> float:
        if self._raw_sensor_value is None:
            return None

        # Normalize the raw sensor value to the range [-1, 1]
        # Clamp the normalized value to [0, 1] and then scale to [-1, 1]
        normalized_value = (self._raw_sensor_value - self._steering_limits.min) / (
            self._steering_limits.max - self._steering_limits.min
        )
        clamped_value = max(0.0, min(1.0, normalized_value))
        return clamped_value * 2.0 - 1.0

    def update(self):
        """Drain the serial buffer and keep only the latest telemetry line."""

        self._buffer += self._serial.read(self._serial.in_waiting or 1)
        # Keep in lines only complete chunks
        *lines, self._buffer = self._buffer.split(b"\n")
        if len(self._buffer) > 256:  # Clean buffer if no newline for too long
            self._buffer = b""

        for line in lines:
            parts = line.decode(errors="ignore").strip().split(",")
            if len(parts) == 4 and parts[0] == "T":
                try:
                    self._raw_sensor_value = int(parts[1])
                    self._left_limit_triggered = parts[2] == "1"
                    self._right_limit_triggered = parts[3] == "1"
                    self._last_rx = time.monotonic()
                except ValueError:
                    pass

    def shutdown(self):
        self.steer(0.0)
        self._serial.close()
