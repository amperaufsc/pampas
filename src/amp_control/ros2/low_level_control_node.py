import rclpy
from can_classes.can_reader import StateCanReader
from hil import ArduinoHIL
from longitudinal_control.PD_controller import PDController
from rclpy.node import Node
from std_msgs.msg import Float32

from fs_msgs.msg import ControlCommand


class LowLevelControl(Node):
    def __init__(self):
        super().__init__("low_level_control")

        self.high_level_control_sub = self.create_subscription(
            ControlCommand, "/control", self.control_callback, 10
        )

        self.pub_sensor = self.create_publisher(Float32, "sensor/value", 10)
        self.pub_control_overshoot = self.create_publisher(
            Float32, "control/actual_value", 10
        )
        self.pub_control = self.create_publisher(
            Float32, "control/anti_windup_value", 10
        )
        self.pub_control_error = self.create_publisher(Float32, "control/error", 10)
        self.pub_min = self.create_publisher(Float32, "control/min_value", 10)
        self.pub_max = self.create_publisher(Float32, "control/max_value", 10)

        self.sensor = Float32()
        self.control = Float32()
        self.control_overshoot = Float32()
        self.error = Float32()
        self.min_signal = Float32()
        self.max_signal = Float32()

        self.left = 15
        self.right = 13
        self.pwm = 18

        ts = 1 / 50
        kp = 85.0
        kd = 0.0 * self.ts
        bias = 20.0
        upper_bound = 90.0
        lower_bound = -90.0
        self._controller = PDController(
            kp,
            kd,
            ts,
            bias,
            upper_bound,
            lower_bound,
        )

        # When the control signal is positive, the wheels steer to the left
        self._setpoint = 0
        self._hardware_integration_layer = ArduinoHIL()
        self._sensor_max = 215.0  # Left
        self._sensor_min = 65.0  # Right

        self.can = StateCanReader()
        self.timer = self.create_timer(1 / 50, self.timer_callback)

    def control_callback(self, setpoint: ControlCommand):
        self._setpoint = -setpoint.steering

    def timer_callback(self):
        try:
            message = self.can.can_listener.read_message()
            steering_data = self.can.can_reader(message)

            self.sensor.data = float(
                (2 * (steering_data - self._sensor_min) / (self._sensor_max - self._sensor_min)) - 1
            )

            self.control_overshoot.data, self.control.data, self.error.data = (
                self._controller.update_signal(self._setpoint, self.sensor.data)
            )

            self.pub_sensor.publish(self.sensor)
            self.pub_control.publish(self.control)
            self.pub_control_overshoot.publish(self.control_overshoot)
            self.pub_min.publish(self.min_signal)
            self.pub_max.publish(self.max_signal)
            self.pub_control_error.publish(self.error)

            # if data > (self.sensor_max -4):
            #    limited_control = min(0.0, self.control.data)
            #    self.signals.steer(limited_control)
            # elif data < (self.sensor_min +4):
            #    limited_control = max(0.0, self.control.data)
            #    self.signals.steer(limited_control)
            # else:
            #    self.signals.steer(self.control.data)
            self._hardware_integration_layer.steer(-20)
        except Exception as e:
            self.get_logger().info(f"{e}")
            if message == None:
                self._hardware_integration_layer.steer(0)
        else:
            self.get_logger().info(f"""
Control: {self.control.data, self.control_overshoot.data, self.error.data}
setPoint: {self._setpoint}\nSensor: {self.sensor.data}, {steering_data}""")
        self.sensor = Float32()


def main(args=None):
    rclpy.init()
    low_level_control = LowLevelControl()
    try:
        rclpy.spin(low_level_control)
    except:
        low_level_control._hardware_integration_layer.shutdown()

    finally:
        low_level_control.destroy_node()
        rclpy.shutdown()
        low_level_control.can.can_listener.bus.shutdown()


if __name__ == "__main__":
    main()
