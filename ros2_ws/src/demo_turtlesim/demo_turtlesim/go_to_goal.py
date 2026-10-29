"""
Closed-loop control: read the pose, steer towards a goal, stop when close.

Run:
    ros2 run demo_turtlesim go_to_goal --ros-args -p x:=9.0 -p y:=2.0
"""
import math

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


def wrap(angle):
    """Keep an angle in [-pi, pi]."""
    return math.atan2(math.sin(angle), math.cos(angle))


class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')
        self.names = ('x', 'y', 'tolerance', 'k_linear', 'k_angular')
        for name, value in zip(self.names, (8.0, 8.0, 0.05, 1.5, 6.0)):
            self.declare_parameter(name, value)
        self.pose = None
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_timer(0.05, self.control)

    def on_pose(self, msg):
        self.pose = msg

    def control(self):
        if self.pose is None:
            return
        p = {n: self.get_parameter(n).value for n in self.names}
        dx, dy = p['x'] - self.pose.x, p['y'] - self.pose.y
        distance = math.hypot(dx, dy)
        cmd = Twist()
        if distance > p['tolerance']:
            heading_error = wrap(math.atan2(dy, dx) - self.pose.theta)
            # turn first, then drive: slow down while the heading is wrong
            cmd.linear.x = p['k_linear'] * distance * max(0.0, math.cos(heading_error))
            cmd.angular.z = p['k_angular'] * heading_error
        elif not getattr(self, 'arrived', False):
            self.arrived = True
            self.get_logger().info(f'arrived at ({self.pose.x:.2f}, {self.pose.y:.2f})')
        self.pub.publish(cmd)


def main():
    rclpy.init()
    try:
        rclpy.spin(GoToGoal())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
