from simple_pid import PID

from amp_control.hardware.board import Board
from amp_control.hardware.sensor import PositionSensor

from .steering_actuator import SteeringActuator


class DCMotorSteeringActuator(SteeringActuator):
    def __init__(
        self,
        board: Board,
        controller: PID,
        position_sensor: PositionSensor,
    ):
        super().__init__(board)
        self._controller = controller
        self._sensor = position_sensor

    def update(
        self,
        target_position: float,
        controller_tunings: tuple[float, float, float] | None = None,
    ) -> SteeringActuator.DebugInfo:
        if controller_tunings is not None:
            self._controller.tunings = controller_tunings

        # PID controller uses the setpoint given by the high level controller and the
        # measured steering sensor position to output a motor command (PWM value).
        self._controller.setpoint = target_position
        sensor_position = self._sensor.read()
        motor_command = self._controller(sensor_position) # Bound to [-255, 255]

        if motor_command is None:
            motor_command = 0.0

        self._board.drive(motor_command)

        return SteeringActuator.DebugInfo(
            sensor_position=sensor_position,
            motor_command=motor_command,
            controller_error=sensor_position - motor_command,
        )

    def stop(self) -> None: ...
