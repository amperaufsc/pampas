#!/opt/venv/bin/python

from typing import cast

import rclpy
from amp_control.hardware.actuator import DCMotorSteeringActuator, SteeringActuator
from amp_control.hardware.board import MockBoard
from amp_control.hardware.sensor import AnalogPositionSensor
from rclpy.node import Node, ParameterDescriptor
from simple_pid import PID
from std_msgs import msg as std_msg

from fs_msgs import msg as fs_msg


class ActuatorControlNode(Node):
    def __init__(self):
        super().__init__("acutator_control")

        self._declare_parameters()

        queue_size: int = 10
        self._create_publishers(queue_size)
        self._create_subscribers(queue_size)

        self._steering_actuator = self._build_steering_actuator()
        self._steering_setpoint = cast(
            float, self.get_parameter("steering_actuator_controller.setpoint").value
        )

    @property
    def steering_actuator(self) -> SteeringActuator:
        return self._steering_actuator

    def update_setpoint_callback(self, setpoint: fs_msg.ControlCommand):
        self._steering_setpoint = setpoint.steering

    def timer_callback(self):
        debug_info = self._steering_actuator.update(self._steering_setpoint)
        print(debug_info)

        # Debugging information
        self._steering_sensor_pub.publish(
            std_msg.Float32(data=debug_info.sensor_position)
        )
        self._controller_output_pub.publish(
            std_msg.Float32(data=debug_info.motor_command)
        )
        self._controller_error_pub.publish(
            std_msg.Float32(data=debug_info.controller_error)
        )


    def _create_subscribers(self, queue_size: int) -> None:
        self._motion_control_sub = self.create_subscription(
            fs_msg.ControlCommand, "/control", self.update_setpoint_callback, queue_size
        )

    def _create_publishers(self, queue_size: int) -> None:
        self._steering_sensor_pub = self.create_publisher(
            std_msg.Float32, "~/debug/steering_sensor", queue_size
        )
        self._controller_output_pub = self.create_publisher(
            std_msg.Float32, "~/debug/controller_output", queue_size
        )
        self._controller_error_pub = self.create_publisher(
            std_msg.Float32, "~/debug/controller_error", queue_size
        )

        self.actuation_timer = self.create_timer(
            1.0 / cast(int, self.get_parameter("update_rate_hz").value),
            self.timer_callback,
        )

    def _declare_parameters(self) -> None:
        self.declare_parameter("update_rate_hz", 100, ParameterDescriptor())
        self.declare_parameter("board", "mock", ParameterDescriptor())
        self.declare_parameter("steering_actuator", "dc_motor", ParameterDescriptor())

        self.declare_parameters(
            namespace="steering_actuator_controller",
            parameters=[
                ("kp", 0.0, ParameterDescriptor()),
                ("ki", 0.0, ParameterDescriptor()),
                ("kd", 0.0, ParameterDescriptor()),
                ("setpoint", 0.0, ParameterDescriptor()),
                ("left_command_limit", -255.0, ParameterDescriptor()),
                ("right_command_limit", 255.0, ParameterDescriptor()),
            ],
        )

        self.declare_parameters(
            namespace="position_sensor",
            parameters=[
                ("min", 0, ParameterDescriptor()),
                ("center", 612, ParameterDescriptor()),
                ("max", 1024, ParameterDescriptor()),
            ],
        )

    def _build_steering_actuator(self) -> SteeringActuator:
        board = MockBoard()
        position_sensor = AnalogPositionSensor(
            board,
            cast(int, self.get_parameter("position_sensor.min").value),
            cast(int, self.get_parameter("position_sensor.center").value),
            cast(int, self.get_parameter("position_sensor.max").value),
        )
        controller = PID(
            Kp=float(
                cast(float, self.get_parameter("steering_actuator_controller.kp").value)
            ),
            Ki=float(
                cast(float, self.get_parameter("steering_actuator_controller.ki").value)
            ),
            Kd=float(
                cast(float, self.get_parameter("steering_actuator_controller.kd").value)
            ),
            output_limits=(
                cast(
                    float,
                    self.get_parameter(
                        "steering_actuator_controller.left_command_limit"
                    ).value,
                ),
                cast(
                    float,
                    self.get_parameter(
                        "steering_actuator_controller.right_command_limit"
                    ).value,
                ),
            ),
            setpoint=cast(
                float,
                self.get_parameter("steering_actuator_controller.setpoint").value,
            ),
            sample_time=0.0,  # The time is controlled by the node timer
        )

        return DCMotorSteeringActuator(
            board=board, controller=controller, position_sensor=position_sensor
        )


def main():
    rclpy.init()
    actuator_control_node = ActuatorControlNode()

    try:
        rclpy.spin(actuator_control_node)
    except RuntimeError:
        actuator_control_node.steering_actuator.stop()
    finally:
        actuator_control_node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
