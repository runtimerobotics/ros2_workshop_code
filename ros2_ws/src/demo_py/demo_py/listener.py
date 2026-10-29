"""
Subscribe to /chatter and log every message.

Run:
    ros2 run demo_py listener
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.sub = self.create_subscription(
            String, 'chatter', self.on_msg, 10)

    def on_msg(self, msg):
        self.get_logger().info(f'I heard: {msg.data}')


def main():
    rclpy.init()
    try:
        rclpy.spin(Listener())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
