"""Plain functions with no ROS in them, so they can be tested without starting ROS."""


def clamp(value, low, high):
    return max(low, min(value, high))
