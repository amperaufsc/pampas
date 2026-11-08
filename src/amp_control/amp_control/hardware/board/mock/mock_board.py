import logging

from ..board import Board

logger = logging.getLogger(__name__)


class MockBoard(Board):
    def __init__(self) -> None: ...

    def drive(self, duty: float) -> None:
        ...

    def read_analog(self) -> int:
        return 0

    def limit_switches(self) -> tuple[bool, bool]:
        return False, False

    def close(self) -> None:
        logger.info("Shutting down MockHardwareInterface")
