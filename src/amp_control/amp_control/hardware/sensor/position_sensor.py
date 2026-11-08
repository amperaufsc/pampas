from abc import ABC, abstractmethod

from amp_control.hardware.board import Board


class PositionSensor(ABC):
    @abstractmethod
    def read(self) -> float: ...


class AnalogPositionSensor(PositionSensor):
    def __init__(
        self, board: Board, raw_min: int, raw_center: int, raw_max: int
    ) -> None:
        self._board = board

        if raw_min < 0:
            raise ValueError(f"raw_min must be >= 0, got {raw_min}")
        if raw_center <= raw_min:
            raise ValueError(f"raw_center must be > {raw_min}, got {raw_center}")
        if raw_max <= raw_center:
            raise ValueError(f"raw_max must be > {raw_center}, got {raw_max}")

        self._min = raw_min
        self._center = raw_center
        self._max = raw_max

    def read(self) -> float:
        raw = self._board.read_analog()
        if raw >= self._center:
            value = (raw - self._center) / (self._max - self._center)
        else:
            value = (raw - self._center) / (self._center - self._min)
        return float(min(1.0, max(value, -1.0)))


# class CanPositionSensor(PositionSensor):
#     def __init__(self, bus: CanBus, signal_name: str, max_age: float) -> None:
#         self._bus = bus
#         self._signal = signal_name
#         self._max_age = max_age

#     def read(self) -> float: ...
