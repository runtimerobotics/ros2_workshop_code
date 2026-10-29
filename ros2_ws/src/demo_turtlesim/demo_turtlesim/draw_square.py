"""
Draw a square by visiting four corners with go-to-goal control (the slide challenge).

Run:
    ros2 run turtlesim turtlesim_node
    ros2 run demo_turtlesim draw_square --ros-args -p side:=4.0
"""
import math

from demo_turtlesim.go_to_goal import wrap
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


def square_corners(x, y, side):
    return [(x, y), (x + side, y), (x + side, y + side), (x, y + side)]


class DrawSquare(Node):
    def __init__(self):
        super().__init__('draw_square')
        self.declare_parameter('side', 4.0)
        self.declare_parameter('laps', 1)
        self.pose = None
        self.corners = []
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_timer(0.05, self.control)

    def on_pose(self, msg):
        if self.pose is None:   # plan the square from wherever the turtle starts
            side, laps = self.get_parameter('side').value, self.get_parameter('laps').value
            corners = square_corners(msg.x, msg.y, side)
            self.corners = (corners[1:] + corners[:1]) * laps
            self.get_logger().info(f'{len(self.corners)} corners to visit')
        self.pose = msg

    def control(self):
        if self.pose is None:
            return
        cmd = Twist()
        if self.corners:
            gx, gy = self.corners[0]
            dx, dy = gx - self.pose.x, gy - self.pose.y
            error = wrap(math.atan2(dy, dx) - self.pose.theta)
            if math.hypot(dx, dy) < 0.05:
                self.corners.pop(0)
                self.get_logger().info(f'corner reached, {len(self.corners)} left')
            elif abs(error) > 0.05:      # rotate on the spot, then drive straight: sharp corners
                cmd.angular.z = 4.0 * error
            else:
                cmd.linear.x = min(2.0, 2.0 * math.hypot(dx, dy))
                cmd.angular.z = 4.0 * error
        self.pub.publish(cmd)


def main():
    rclpy.init()
    try:
        rclpy.spin(DrawSquare())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
