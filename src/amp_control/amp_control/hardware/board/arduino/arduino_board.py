import time

import serial as pyserial

from ..board import Board


class ArduinoBoard(Board):
    """Hardware integration layer for Arduino."""

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        baud: int = 115200,
    ):
        self._serial = pyserial.Serial(port, baud, timeout=0.01)
        self._buffer = b""
        self._last_rx = None
        self._raw_sensor_value = -1
        self._left_limit_triggered = False
        self._right_limit_triggered = False

    def drive(self, duty: float) -> None:
        self._serial.write(f"S,{int(duty)}\n".encode())

    def read_analog(self) -> int:
        self._update()
        return self._raw_sensor_value

    def _update(self):
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

    def close(self):
        self.drive(0.0)
        self._serial.close()
