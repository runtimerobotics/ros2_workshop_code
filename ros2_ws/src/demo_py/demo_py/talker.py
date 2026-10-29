"""
Publish a String on /chatter every 0.5 s.

Run:
    ros2 run demo_py talker
    ros2 topic echo /chatter
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.pub = self.create_publisher(
            String, 'chatter', 10)
        self.timer = self.create_timer(0.5, self.tick)
        self.count = 0

    def tick(self):
        msg = String(data=f'Hello {self.count}')
        self.pub.publish(msg)
        self.count += 1


def main():
    rclpy.init()
    try:
        rclpy.spin(Talker())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
