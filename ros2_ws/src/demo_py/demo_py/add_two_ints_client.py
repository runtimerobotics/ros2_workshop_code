"""
Service client: ask the server to add 2 and 3, without blocking, then exit.

Run:
    ros2 run demo_py add_two_ints_server
    ros2 run demo_py add_two_ints_client       # sum: 5
"""
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for service...')

    def send_request(self, a, b):
        req = AddTwoInts.Request(a=a, b=b)
        return self.cli.call_async(req)


def main():
    rclpy.init()
    client = MinimalClientAsync()
    future = client.send_request(2, 3)
    rclpy.spin_until_future_complete(client, future)
    client.get_logger().info(f'sum: {future.result().sum}')
    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
