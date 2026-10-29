"""
Publish fixed sensor mounts once on /tf_static: static_transform_publisher, as a node.

Run:
    ros2 run demo_tf2 static_frames
    ros2 run tf2_ros tf2_echo base_link lidar_link
"""
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


def mount(node, parent, child, x, y, z):
    t = TransformStamped()
    t.header.stamp = node.get_clock().now().to_msg()
    t.header.frame_id = parent
    t.child_frame_id = child
    t.transform.translation.x, t.transform.translation.y, t.transform.translation.z = x, y, z
    t.transform.rotation.w = 1.0   # no rotation
    return t


class StaticFrames(Node):
    def __init__(self):
        super().__init__('static_frames')
        self.tf_static = StaticTransformBroadcaster(self)
        self.tf_static.sendTransform([
            mount(self, 'base_link', 'lidar_link', 0.1, 0.0, 0.2),
            mount(self, 'base_link', 'camera_link', 0.15, 0.0, 0.12),
        ])
        self.get_logger().info('published base_link → lidar_link, camera_link on /tf_static')


def main():
    rclpy.init()
    try:
        rclpy.spin(StaticFrames())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
