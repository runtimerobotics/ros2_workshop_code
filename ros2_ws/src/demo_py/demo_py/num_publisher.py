"""
Publish the custom demo_interfaces/msg/Num message.

Run:
    ros2 run demo_py num_publisher
    ros2 topic echo /num
"""
from demo_interfaces.msg import Num
import rclpy
from rclpy.node import Node


class NumPublisher(Node):

    def __init__(self):
        super().__init__('num_publisher')
        self.pub = self.create_publisher(Num, 'num', 10)
        self.n = 0
        self.create_timer(1.0, self.tick)

    def tick(self):
        self.pub.publish(Num(num=self.n))
        self.n += 1


def main():
    rclpy.init()
    try:
        rclpy.spin(NumPublisher())
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
