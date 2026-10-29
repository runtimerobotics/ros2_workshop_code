"""
Subscribe to /turtle1/pose and warn when the turtle gets close to a wall.

Run:
    ros2 run demo_turtlesim pose_monitor
"""
import rclpy
from rclpy.node import Node

try:                                    # Kilted and newer: turtlesim_msgs
    from turtlesim_msgs.msg import Pose
except ImportError:                     # Jazzy
    from turtlesim.msg import Pose

WORLD = 11.0889   # turtlesim's window is 11.09 m wide and tall


class PoseMonitor(Node):

    def __init__(self):
        super().__init__('pose_monitor')
        self.declare_parameter('margin', 1.0)
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.near = False

    def on_pose(self, msg):
        margin = self.get_parameter('margin').value
        near = min(msg.x, msg.y, WORLD - msg.x, WORLD - msg.y) < margin
        if near != self.near:   # log only when the state changes, not 62 times a second
            self.near = near
            if near:
                self.get_logger().warning(f'near a wall at x={msg.x:.2f} y={msg.y:.2f}')
            else:
                self.get_logger().info('clear of the walls')


def main():
    rclpy.init()
    try:
        rclpy.spin(PoseMonitor())
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
