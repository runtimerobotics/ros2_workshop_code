"""
Find coloured boxes in the RealSense colour image and publish where they are in 3D.

For each colour: threshold in HSV, keep the largest blob, read the aligned depth at its
centre, back-project with the camera intrinsics, and transform into the world frame.

Run:
    ros2 run demo_arm_vision object_detector
Publishes:
    /detections/<colour>   geometry_msgs/PoseStamped   box centre in world
    /detections/image      sensor_msgs/Image           camera image with the detections drawn
    /detections/markers    visualization_msgs/MarkerArray
"""
import math

import cv2
from cv_bridge import CvBridge
from demo_arm_vision.geometry import grasp_yaw, pixel_to_point
from geometry_msgs.msg import PointStamped, PoseStamped
import message_filters
import numpy as np
import rclpy
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image
import tf2_geometry_msgs  # noqa: F401  (registers PointStamped with tf2)
from tf2_ros import Buffer, TransformException, TransformListener
from visualization_msgs.msg import Marker, MarkerArray

DRAW = {'red': (0, 0, 255), 'blue': (255, 0, 0), 'green': (0, 200, 0), 'yellow': (0, 220, 220)}


class ObjectDetector(Node):

    def __init__(self):
        super().__init__('object_detector')
        self.target_frame = self.declare_parameter('target_frame', 'world').value
        self.min_area = self.declare_parameter('min_area', 80).value
        self.box_size = self.declare_parameter('box_size', 0.04).value
        self.colors = self.declare_parameter('colors', ['red', 'blue']).value
        self.ranges = {}
        for c in self.colors:
            flat = self.declare_parameter(f'{c}_ranges', [0, 0, 0, 0, 0, 0]).value
            # every 6 numbers are one range: low H S V, high H S V
            self.ranges[c] = [(np.array(flat[i:i + 3]), np.array(flat[i + 3:i + 6]))
                              for i in range(0, len(flat), 6)]
        self.bridge = CvBridge()
        self.tf = Buffer()
        self.tf_listener = TransformListener(self.tf, self)
        self.info = None
        qos = qos_profile_sensor_data
        self.create_subscription(CameraInfo, '/camera/camera/color/camera_info', self.on_info, qos)
        # colour and depth arrive separately: pair the images taken at the same time
        color = message_filters.Subscriber(
            self, Image, '/camera/camera/color/image_raw', qos_profile=qos)
        depth = message_filters.Subscriber(
            self, Image, '/camera/camera/aligned_depth_to_color/image_raw', qos_profile=qos)
        sync = message_filters.ApproximateTimeSynchronizer([color, depth], 5, 0.05)
        sync.registerCallback(self.on_images)
        self.pose_pubs = {c: self.create_publisher(PoseStamped, f'/detections/{c}', 10)
                          for c in self.colors}
        self.image_pub = self.create_publisher(Image, '/detections/image', 1)
        self.marker_pub = self.create_publisher(MarkerArray, '/detections/markers', 1)
        self.get_logger().info(f'looking for {", ".join(self.colors)} boxes')

    def on_info(self, msg):
        self.info = msg

    def find(self, hsv, color):
        """Return the largest blob of this colour as (cx, cy, angle, contour), or None."""
        mask = sum(cv2.inRange(hsv, lo, hi) for lo, hi in self.ranges[color])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if cv2.contourArea(c) >= self.min_area]
        if not contours:
            return None
        best = max(contours, key=cv2.contourArea)
        (cx, cy), _, angle = cv2.minAreaRect(best)
        return cx, cy, angle, best

    def depth_at(self, depth, u, v):
        """Median depth in metres in a 5x5 window: robust to noise and missing pixels."""
        patch = depth[max(0, v - 2):v + 3, max(0, u - 2):u + 3].astype(np.float32)
        if depth.dtype == np.uint16:      # a real RealSense publishes millimetres
            patch = patch / 1000.0
        patch = patch[np.isfinite(patch) & (patch > 0)]
        return float(np.median(patch)) if patch.size else None

    def on_images(self, color_msg, depth_msg):
        if self.info is None:
            return
        image = self.bridge.imgmsg_to_cv2(color_msg, 'bgr8')
        depth = self.bridge.imgmsg_to_cv2(depth_msg)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        fx, fy, cx0, cy0 = self.info.k[0], self.info.k[4], self.info.k[2], self.info.k[5]
        markers = MarkerArray()
        for i, color in enumerate(self.colors):
            found = self.find(hsv, color)
            if found is None:
                continue
            u, v, angle, contour = found
            z = self.depth_at(depth, int(round(u)), int(round(v)))
            if z is None:
                continue
            point = PointStamped()
            point.header = color_msg.header
            point.point.x, point.point.y, point.point.z = pixel_to_point(u, v, z, fx, fy, cx0, cy0)
            try:
                p = self.tf.transform(point, self.target_frame,
                                      timeout=Duration(seconds=0.1)).point
            except TransformException as ex:
                self.get_logger().warning(f'no transform to {self.target_frame}: {ex}',
                                          throttle_duration_sec=5.0)
                return
            # the camera sees the top face: the box centre is half a box lower
            pose = PoseStamped()
            pose.header.frame_id, pose.header.stamp = self.target_frame, color_msg.header.stamp
            centre = pose.pose.position
            centre.x, centre.y, centre.z = p.x, p.y, p.z - self.box_size / 2
            # the box's yaw about world z; image x is world -y, so the image angle flips sign
            yaw = grasp_yaw(-angle)
            pose.pose.orientation.z, pose.pose.orientation.w = math.sin(yaw / 2), math.cos(yaw / 2)
            self.pose_pubs[color].publish(pose)
            markers.markers.append(self.marker(i, color, pose))
            cv2.drawContours(image, [contour], -1, DRAW.get(color, (255, 255, 255)), 2)
            cv2.putText(image, f'{color} ({p.x:.2f}, {p.y:.2f})', (int(u) + 12, int(v)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (20, 20, 20), 1, cv2.LINE_AA)
        self.marker_pub.publish(markers)
        out = self.bridge.cv2_to_imgmsg(image, 'bgr8')
        out.header = color_msg.header
        self.image_pub.publish(out)

    def marker(self, i, color, pose):
        m = Marker(type=Marker.CUBE, action=Marker.ADD, id=i, ns='detections')
        m.header = pose.header
        m.pose = pose.pose
        m.scale.x = m.scale.y = m.scale.z = self.box_size
        r, g, b = (c / 255.0 for c in reversed(DRAW.get(color, (255, 255, 255))))
        m.color.r, m.color.g, m.color.b, m.color.a = r, g, b, 0.6
        m.lifetime.sec = 1
        return m


def main():
    rclpy.init()
    try:
        rclpy.spin(ObjectDetector())
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
