"""
Action client for /turtle1/rotate_absolute: feedback while turning, optional cancel.

Run:
    ros2 run demo_turtlesim rotate_turtle --ros-args -p theta:=3.14
    ros2 run demo_turtlesim rotate_turtle --ros-args -p theta:=-1.57 -p cancel_after:=0.5
"""
from action_msgs.msg import GoalStatus
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from turtlesim.action import RotateAbsolute


class RotateTurtle(Node):
    def __init__(self):
        super().__init__('rotate_turtle')
        self.declare_parameter('theta', 3.14)
        self.declare_parameter('cancel_after', 0.0)   # seconds; 0 = never cancel
        self.client = ActionClient(self, RotateAbsolute, '/turtle1/rotate_absolute')
        self.goal_handle = None

    def start(self):
        if not self.client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('rotate_absolute is not available: is turtlesim running?')
            rclpy.shutdown()
            return
        goal = RotateAbsolute.Goal(theta=self.get_parameter('theta').value)
        future = self.client.send_goal_async(goal, feedback_callback=self.on_feedback)
        future.add_done_callback(self.on_accepted)

    def on_feedback(self, msg):
        self.get_logger().info(f'remaining: {msg.feedback.remaining:.2f} rad')

    def on_accepted(self, future):
        self.goal_handle = future.result()
        if not self.goal_handle.accepted:
            self.get_logger().warn('goal rejected')
            rclpy.shutdown()
            return
        self.get_logger().info('goal accepted')
        self.goal_handle.get_result_async().add_done_callback(self.on_result)
        delay = self.get_parameter('cancel_after').value
        if delay > 0:
            self.cancel_timer = self.create_timer(delay, self.cancel)

    def cancel(self):
        self.cancel_timer.cancel()
        self.get_logger().info('canceling the goal')
        self.goal_handle.cancel_goal_async()

    def on_result(self, future):
        status = {GoalStatus.STATUS_SUCCEEDED: 'SUCCEEDED', GoalStatus.STATUS_CANCELED: 'CANCELED',
                  GoalStatus.STATUS_ABORTED: 'ABORTED'}.get(future.result().status, 'UNKNOWN')
        self.get_logger().info(f'{status}: delta {future.result().result.delta:.2f} rad')
        rclpy.shutdown()


def main():
    rclpy.init()
    node = RotateTurtle()
    node.start()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
