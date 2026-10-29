"""
Publish a fixed sensor mount once on /tf_static: static_transform_publisher, as a node.

Run:
    ros2 run demo_tf2 static_frames
    ros2 run tf2_ros tf2_echo base_link lidar_link
"""
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import (
    StaticTransformBroadcaster)


class StaticFrames(Node):
    def __init__(self):
        super().__init__('static_frames')
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'lidar_link'
        t.transform.translation.x = 0.1
        t.transform.translation.z = 0.2
        t.transform.rotation.w = 1.0
        self.tf_static = StaticTransformBroadcaster(self)
        self.tf_static.sendTransform(t)


def main():
    rclpy.init()
    try:
        rclpy.spin(StaticFrames())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
