#!/opt/venv/bin/python

from typing import cast

import rclpy
from amp_control.hardware import (
    HardwareInterface,
    HardwareInterfaceOption,
    SteeringLimits,
    ThrottleLimits,
    hardware_controller_factory,
)
from rclpy.node import Node, ParameterDescriptor
from simple_pid import PID
from std_msgs.msg import Float32

from fs_msgs.msg import ControlCommand


class LowLevelControl(Node):
    def __init__(self):
        super().__init__("low_level_control")

        self.declare_parameters(
            namespace="steering_actuator_controller",
            parameters=[
                ("kp", 0.0, ParameterDescriptor()),
                ("ki", 0.0, ParameterDescriptor()),
                ("kd", 0.0, ParameterDescriptor()),
                ("setpoint", 0.0, ParameterDescriptor()),
                ("left_position_limit", -90.0, ParameterDescriptor()),
                ("right_position_limit", 90.0, ParameterDescriptor()),
            ],
        )

        self._steering_actuator_controller = PID(
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
                        "steering_actuator_controller.left_position_limit"
                    ).value,
                ),
                cast(
                    float,
                    self.get_parameter(
                        "steering_actuator_controller.right_position_limit"
                    ).value,
                ),
            ),
            setpoint=cast(
                float,
                self.get_parameter("steering_actuator_controller.setpoint").value,
            ),
            sample_time=0.0,  # The time is controlled by the node timer
        )

        self._hardware_controller: HardwareInterface = hardware_controller_factory(
            HardwareInterfaceOption.ARDUINO,
            ThrottleLimits(min=0.0, max=1.0),
            SteeringLimits(min=-1.0, max=1.0),
        )

        self.declare_parameter(
            name="low_level_control/steering_sensor_max",
            value=1024,
            descriptor=ParameterDescriptor(),
        )

        # --- Publishers and Subscribers ---

        queue_size: int = 10
        self.high_level_control_sub = self.create_subscription(
            ControlCommand, "/control", self.control_callback, queue_size
        )
        # Debug topics
        self._steering_sensor_pub = self.create_publisher(
            Float32, "~/debug/steering_sensor", queue_size
        )
        self._controller_output_pub = self.create_publisher(
            Float32, "~/debug/controller_output", queue_size
        )
        self._controller_error_pub = self.create_publisher(
            Float32, "~/debug/controller_error", queue_size
        )

        self.timer = self.create_timer(1 / 50, self.timer_callback)

    def control_callback(self, setpoint: ControlCommand):
        pass
        # self._setpoint = -setpoint.steering

    def timer_callback(self):
        reference_position: float = 0.0 # TODO: Receive value from high level control
        self._steering_actuator_controller.setpoint = reference_position
        sensor_position = self._hardware_controller.steering_position()
        output = self._steering_actuator_controller(sensor_position)

        if output is None:
            raise RuntimeError("wtf")

        # Debugging information
        self._steering_sensor_pub.publish(sensor_position)
        self._controller_output_pub.publish(output)
        self._controller_error_pub.publish(sensor_position - output)

        self._hardware_controller.steer(reference_position)


def main():
    rclpy.init()
    low_level_control = LowLevelControl()

    try:
        rclpy.spin(low_level_control)
    except RuntimeError:
        low_level_control._hardware_controller.shutdown()
    finally:
        low_level_control.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
