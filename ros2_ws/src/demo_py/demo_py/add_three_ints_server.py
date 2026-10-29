"""
Service server for the custom demo_interfaces/srv/AddThreeInts.

Run:
    ros2 run demo_py add_three_ints_server
    ros2 service call /add_three_ints demo_interfaces/srv/AddThreeInts "{a: 1, b: 2, c: 3}"
"""
from demo_interfaces.srv import AddThreeInts
import rclpy
from rclpy.node import Node


class AddThreeIntsServer(Node):
    def __init__(self):
        super().__init__('add_three_ints_server')
        self.srv = self.create_service(AddThreeInts, 'add_three_ints', self.add)

    def add(self, request, response):
        response.sum = request.a + request.b + request.c
        self.get_logger().info(f'{request.a} + {request.b} + {request.c} = {response.sum}')
        return response


def main():
    rclpy.init()
    try:
        rclpy.spin(AddThreeIntsServer())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
