"""Small geometry helpers with no ROS in them, so they can be unit tested."""
import math


def pixel_to_point(u, v, depth, fx, fy, cx, cy):
    """Back-project pixel (u, v) at a depth into the camera optical frame (z forward)."""
    return ((u - cx) * depth / fx, (v - cy) * depth / fy, depth)


def top_down_quaternion(yaw):
    """Quaternion (x, y, z, w) for a tool pointing straight down, rotated by yaw about world z."""
    return (math.cos(yaw / 2), math.sin(yaw / 2), 0.0, 0.0)


def grasp_yaw(angle_deg):
    """
    Gripper yaw for a box seen at an image angle (from cv2.minAreaRect).

    A square box looks the same every 90°, so pick the equivalent angle closest to 0:
    the wrist then turns as little as possible.
    """
    a = math.radians(angle_deg) % (math.pi / 2)
    return a - math.pi / 2 if a > math.pi / 4 else a
