from abc import ABC, abstractmethod
from dataclasses import dataclass

from amp_control.hardware.board import Board
from amp_control.hardware.sensor import PositionSensor


class SteeringActuator(ABC):
    @dataclass
    class DebugInfo:
        sensor_position: float
        motor_command: float
        controller_error: float

    def __init__(self, board: Board, sensor: PositionSensor):
        self._board = board
        self._sensor = sensor

    @abstractmethod
    def update(self, target_position: float) -> DebugInfo: ...
    @abstractmethod
    def stop(self) -> None: ...

    @property
    def board(self) -> Board:
        return self._board
