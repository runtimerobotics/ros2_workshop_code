"""
Action client: send a goal, print feedback, print the result, then exit.

Run:
    ros2 run demo_py fibonacci_action_client 10
"""
import sys

from demo_interfaces.action import Fibonacci
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        self._client.wait_for_server()
        future = self._client.send_goal_async(
            Fibonacci.Goal(order=order),
            feedback_callback=self.on_feedback)
        future.add_done_callback(self.on_goal_response)

    def on_feedback(self, msg):
        self.get_logger().info(f'{list(msg.feedback.partial_sequence)}')

    def on_goal_response(self, future):
        handle = future.result()
        if not handle.accepted:
            self.get_logger().info('goal rejected')
            rclpy.shutdown()
            return
        handle.get_result_async().add_done_callback(self.on_result)

    def on_result(self, future):
        self.get_logger().info(f'result: {list(future.result().result.sequence)}')
        rclpy.shutdown()   # done: let main() return


def main():
    rclpy.init()
    order = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    client = FibonacciActionClient()
    client.send_goal(order)
    try:
        rclpy.spin(client)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
