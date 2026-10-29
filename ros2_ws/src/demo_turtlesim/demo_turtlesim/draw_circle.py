"""
Publish a constant Twist so turtle1 drives in a circle (radius = v / w).

Run:
    ros2 run turtlesim turtlesim_node
    ros2 run demo_turtlesim draw_circle --ros-args -p linear:=2.0 -p angular:=1.0
"""
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node


class DrawCircle(Node):
    def __init__(self):
        super().__init__('draw_circle')
        self.declare_parameter('linear', 2.0)    # m/s, along x (forward)
        self.declare_parameter('angular', 1.0)   # rad/s, about z (counter-clockwise)
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_timer(0.1, self.tick)
        v, w = self.get_parameter('linear').value, self.get_parameter('angular').value
        self.get_logger().info(f'circle radius {abs(v / w):.2f} m' if w else 'straight line')

    def tick(self):
        msg = Twist()
        msg.linear.x = self.get_parameter('linear').value
        msg.angular.z = self.get_parameter('angular').value
        self.pub.publish(msg)


def main():
    rclpy.init()
    try:
        rclpy.spin(DrawCircle())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
