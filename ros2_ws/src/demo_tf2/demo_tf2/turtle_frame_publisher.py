"""
Broadcast world → <turtle> from the turtle's pose, on every pose message.

Run:
    ros2 run turtlesim turtlesim_node
    ros2 run demo_tf2 turtle_frame_publisher --ros-args -p turtlename:=turtle1
    ros2 run tf2_ros tf2_echo world turtle1
"""
import math

from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose


class FramePublisher(Node):
    def __init__(self):
        super().__init__('turtle_tf2_frame_publisher')
        self.turtlename = self.declare_parameter('turtlename', 'turtle1').value
        self.br = TransformBroadcaster(self)
        self.create_subscription(
            Pose, f'/{self.turtlename}/pose', self.on_pose, 1)

    def on_pose(self, msg):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.turtlename
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.rotation.z = math.sin(msg.theta / 2)
        t.transform.rotation.w = math.cos(msg.theta / 2)
        self.br.sendTransform(t)


def main():
    rclpy.init()
    try:
        rclpy.spin(FramePublisher())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
