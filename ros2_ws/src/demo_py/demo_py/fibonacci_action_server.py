"""
Action server: compute a Fibonacci sequence, one number per second, with feedback.

Run:
    ros2 run demo_py fibonacci_action_server
    ros2 action send_goal --feedback fibonacci demo_interfaces/action/Fibonacci "{order: 5}"
"""
import time

from demo_interfaces.action import Fibonacci
import rclpy
from rclpy.action import ActionServer, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._server = ActionServer(
            self, Fibonacci, 'fibonacci', self.execute,
            cancel_callback=lambda goal: CancelResponse.ACCEPT)

    def execute(self, goal_handle):
        self.get_logger().info(f'goal: order {goal_handle.request.order}')
        fb = Fibonacci.Feedback(partial_sequence=[0, 1])
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('goal canceled')
                return Fibonacci.Result(sequence=fb.partial_sequence)
            fb.partial_sequence.append(fb.partial_sequence[i] + fb.partial_sequence[i - 1])
            goal_handle.publish_feedback(fb)
            time.sleep(1)
        goal_handle.succeed()
        return Fibonacci.Result(sequence=fb.partial_sequence)


def main():
    rclpy.init()
    try:
        # several threads, so a cancel request is handled while execute() runs
        rclpy.spin(FibonacciActionServer(), executor=MultiThreadedExecutor())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
