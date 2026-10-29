"""
A timer calls on_timer every 0.5 s.

Run:
    ros2 run demo_py heartbeat
"""
import rclpy
from rclpy.node import Node


class Heartbeat(Node):
    def __init__(self):
        super().__init__('heartbeat')
        self.timer = self.create_timer(0.5, self.on_timer)

    def on_timer(self):
        self.get_logger().info('alive')


def main():
    rclpy.init()
    try:
        rclpy.spin(Heartbeat())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
