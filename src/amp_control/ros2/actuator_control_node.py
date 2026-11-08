#!/opt/venv/bin/python

from typing import cast

import rclpy
from amp_control.hardware.actuator import DCMotorSteeringActuator, SteeringActuator
from amp_control.hardware.board import MockBoard
from amp_control.hardware.sensor import AnalogPositionSensor
from rclpy.node import Node, ParameterDescriptor
from simple_pid import PID

from amp_msgs import msg as amp_msgs
from fs_msgs import msg as fs_msg


class ActuatorControlNode(Node):
    def __init__(self):
        super().__init__("acutator_control")
        self.get_logger().info("Starting node...")

        # Must come before any call of self.get_parameter
        self._declare_parameters()

        queue_size: int = 10
        self._motion_control_sub = self.create_subscription(
            fs_msg.ControlCommand, "/control", self.update_setpoint_callback, queue_size
        )
        self._debug_pub = self.create_publisher(
            amp_msgs.SteeringActuatorControlDebug,
            "/debug/steering_actuator/control",
            queue_size,
        )

        self._steering_actuator = self._build_steering_actuator()
        self._steering_setpoint = cast(
            float, self.get_parameter("steering_actuator_controller.setpoint").value
        )

        self.actuation_timer = self.create_timer(
            1.0 / cast(int, self.get_parameter("update_rate_hz").value),
            self.timer_callback,
        )

        self.get_logger().info("Node started")

    def update_setpoint_callback(self, setpoint: fs_msg.ControlCommand):
        self._steering_setpoint = setpoint.steering

    def timer_callback(self):
        controller_tunings = (
            cast(float, self.get_parameter("steering_actuator_controller.kp").value),
            cast(float, self.get_parameter("steering_actuator_controller.ki").value),
            cast(float, self.get_parameter("steering_actuator_controller.kd").value),
        )
        debug_info = self._steering_actuator.update(
            self._steering_setpoint,
            controller_tunings=controller_tunings
        )
        self._publish_debug(debug_info)

    @property
    def steering_actuator(self) -> SteeringActuator:
        return self._steering_actuator

    def _declare_parameters(self) -> None:
        self.declare_parameter("update_rate_hz", 100, ParameterDescriptor())
        self.declare_parameter("board", "mock", ParameterDescriptor())
        self.declare_parameter("steering_actuator", "dc_motor", ParameterDescriptor())

        self.declare_parameters(
            namespace="steering_actuator_controller",
            parameters=[
                ("kp", 100.0, ParameterDescriptor()),
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
        position_sensor = AnalogPositionSensor(
            board,
            cast(int, self.get_parameter("position_sensor.min").value),
            cast(int, self.get_parameter("position_sensor.center").value),
            cast(int, self.get_parameter("position_sensor.max").value),
        )

        return DCMotorSteeringActuator(
            board=board, sensor=position_sensor, controller=controller
        )

    def _publish_debug(self, debug_info: SteeringActuator.DebugInfo):
        msg = amp_msgs.SteeringActuatorControlDebug()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.sensor_position = debug_info.sensor_position
        msg.motor_command = debug_info.motor_command
        msg.controller_error = debug_info.controller_error
        self._debug_pub.publish(msg)


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
