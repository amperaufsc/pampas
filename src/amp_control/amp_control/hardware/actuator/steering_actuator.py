from abc import ABC, abstractmethod
from dataclasses import dataclass

from amp_control.hardware.board import Board


class SteeringActuator(ABC):
    @dataclass
    class DebugInfo:
        sensor_position: float
        motor_command: float
        controller_error: float

    def __init__(self, board: Board):
        self._board = board

    @abstractmethod
    def update(self, target_position: float) -> DebugInfo: ...
    @abstractmethod
    def stop(self) -> None: ...
