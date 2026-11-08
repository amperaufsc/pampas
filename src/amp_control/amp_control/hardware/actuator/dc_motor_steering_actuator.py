from simple_pid import PID

from amp_control.hardware.board import Board
from amp_control.hardware.sensor import PositionSensor

from .steering_actuator import SteeringActuator


class DCMotorSteeringActuator(SteeringActuator):
    def __init__(
        self,
        board: Board,
        sensor: PositionSensor,
        controller: PID,
    ):
        super().__init__(board, sensor)
        self._controller = controller

    def update(
        self,
        target_position: float,
        controller_tunings: tuple[float, float, float] | None = None,
    ) -> SteeringActuator.DebugInfo:
        if controller_tunings is not None:
            self._controller.tunings = controller_tunings
        self._controller.setpoint = target_position

        measured_position = self._sensor.read()
        motor_command = self._controller(measured_position)
        if motor_command is None or -10 < motor_command < 10:
            motor_command = 0.0

        self._board.drive(motor_command)
        self._last_motor_command = motor_command

        return SteeringActuator.DebugInfo(
            sensor_position=measured_position,
            motor_command=motor_command,
            controller_error=target_position - measured_position,
        )


    def stop(self) -> None: ...
