import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_msgs.msg import Float64


class TemperatureNode(Node):
    def __init__(self):
        super().__init__('temperature_node')

        self.ambient_temperature = 0.0
        self.target_temperature = 10.0
        self.hysteresis = 2
        self.heating_rate = 0.4
        self.cooling_rate = 0.09
        self.temperature = 20.0
        self.heater_on = False

        self.temperature_pub = self.create_publisher(Float64, '/temperature', 10)
        self.heater_pub = self.create_publisher(Bool, '/heater_on', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('Temperature node operational')

    def timer_callback(self):
        if self.heater_on and self.temperature >= self.target_temperature + self.hysteresis:
            self.heater_on = False
        elif (not self.heater_on) and self.temperature <= self.target_temperature - self.hysteresis:
            self.heater_on = True

        if self.heater_on:
            self.temperature += self.heating_rate
        else:
            self.temperature -= max(0.0, self.temperature - self.ambient_temperature) * self.cooling_rate

        self.temperature += random.uniform(-0.03, 0.03)
        self.temperature = max(15.0, min(40.0, self.temperature))

        temperature_msg = Float64()
        temperature_msg.data = float(self.temperature)
        heater_msg = Bool()
        heater_msg.data = bool(self.heater_on)

        self.temperature_pub.publish(temperature_msg)
        self.heater_pub.publish(heater_msg)


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()