"""
A slow callback no longer blocks a fast one: MultiThreadedExecutor + callback groups.

Run:
    ros2 run demo_py executor_demo      # control keeps its 0.5 s rhythm
Change MultiThreadedExecutor to SingleThreadedExecutor and the control ticks wait for plan.
"""
import time

import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node


class Robot(Node):

    def __init__(self):
        super().__init__('robot')
        slow = MutuallyExclusiveCallbackGroup()   # one group per timer:
        fast = MutuallyExclusiveCallbackGroup()   # they may run at the same time
        self.create_timer(2.0, self.plan, callback_group=slow)
        self.create_timer(0.5, self.control, callback_group=fast)

    def plan(self):
        time.sleep(1.5)                  # slow work
        self.get_logger().info('plan ready')

    def control(self):
        self.get_logger().info('control tick')


def main():
    rclpy.init()
    try:
        rclpy.spin(Robot(), executor=MultiThreadedExecutor())
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
