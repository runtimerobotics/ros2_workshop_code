"""
A talker whose publish rate is a parameter (the one-command startup lab).

Run:
    ros2 run demo_py rate_talker --ros-args -p rate:=4.0
    ros2 launch demo_py demo.launch.py          # rate from config/params.yaml
    ros2 param set /rate_talker rate 1.0        # changes the timer while running
"""
from rcl_interfaces.msg import FloatingPointRange, ParameterDescriptor
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class RateTalker(Node):

    def __init__(self):
        super().__init__('rate_talker')
        self.declare_parameter('rate', 2.0, ParameterDescriptor(
            description='Messages per second',
            floating_point_range=[FloatingPointRange(from_value=0.1, to_value=50.0)]))
        self.declare_parameter('prefix', 'Hello')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.count = 0
        self.timer = self.create_timer(1.0 / self.get_parameter('rate').value, self.tick)
        self.add_post_set_parameters_callback(self.on_changed)

    def tick(self):
        prefix = self.get_parameter('prefix').value
        self.pub.publish(String(data=f'{prefix} {self.count}'))
        self.count += 1

    def on_changed(self, params):
        for p in params:
            if p.name == 'rate':
                self.timer.cancel()
                self.timer = self.create_timer(1.0 / p.value, self.tick)
                self.get_logger().info(f'rate is now {p.value} Hz')


def main():
    rclpy.init()
    try:
        rclpy.spin(RateTalker())
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
