import logging
import math
import random
import time

from ..board import Board

logger = logging.getLogger(__name__)


class MockBoard(Board):
    def __init__(self) -> None:
        self._actual_position = 0.0
        self._motor_speed = 0.0
        self._last_command = 0.0
        self._last_time = None

        self._min_adc = 0
        self._max_adc = 1024

    def drive(self, duty: float) -> None:
        self._last_command = duty

    def read_analog(self) -> int:
        now = time.monotonic()
        dt = (now - self._last_time) if self._last_time is not None else 0.01
        self._last_time = now

        commanded_speed = (self._last_command / 255.0) * 3.0
        alpha = 1.0 - math.exp(-dt / 0.05)
        self._motor_speed += (commanded_speed - self._motor_speed) * alpha
        self._actual_position += self._motor_speed * dt
        self._actual_position = max(-1.0, min(1.0, self._actual_position))

        normalized_adc = (self._actual_position + 1.0) / 2.0  # -1..1 → 0..1
        adc = self._min_adc + normalized_adc * (self._max_adc - self._min_adc)
        # Add a little noise like a real ADC
        adc += random.gauss(0, 1.5)

        return int(max(self._min_adc, min(self._max_adc, adc)))

    def limit_switches(self) -> tuple[bool, bool]:
        return False, False

    def close(self) -> None:
        logger.info("Shutting down MockBoard")
