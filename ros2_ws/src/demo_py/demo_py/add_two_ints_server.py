"""
Service server: add two integers.

Run:
    ros2 run demo_py add_two_ints_server
    ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
"""
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(
            AddTwoInts, 'add_two_ints', self.add)

    def add(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            f'a: {request.a} b: {request.b}')
        return response


def main():
    rclpy.init()
    try:
        rclpy.spin(MinimalService())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
