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
        self.create_timer(
            2.0, self.plan,
            callback_group=MutuallyExclusiveCallbackGroup())
        self.create_timer(
            0.5, self.control,
            callback_group=MutuallyExclusiveCallbackGroup())

    def plan(self):
        time.sleep(1.5)                  # slow work
        self.get_logger().info('plan ready')

    def control(self):
        self.get_logger().info('control tick')


def main():
    rclpy.init()
    executor = MultiThreadedExecutor()
    executor.add_node(Robot())
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
