#!/usr/bin/env python3
"""
Give Gazebo's RGB-D point cloud the frame its points are really in.

Gazebo puts one frame name on every output of an rgbd_camera. The images need the
optical frame (z forward), but the point cloud is computed in the sensor's own axes
(x forward). This node republishes the cloud with frame camera_color_frame, which has
exactly those axes, under the realsense2_camera topic name.
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import PointCloud2


class PointsFrameFix(Node):
    def __init__(self):
        super().__init__('points_frame_fix')
        self.frame = self.declare_parameter('frame_id', 'camera_color_frame').value
        qos = qos_profile_sensor_data
        self.pub = self.create_publisher(PointCloud2, '/camera/camera/depth/color/points', qos)
        self.create_subscription(PointCloud2, '/camera/gz_points', self.on_cloud, qos)

    def on_cloud(self, msg):
        msg.header.frame_id = self.frame
        self.pub.publish(msg)


def main():
    rclpy.init()
    try:
        rclpy.spin(PointsFrameFix())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
