"""
Open or close the gripper.

Run:
    ros2 run demo_arm_control gripper close
    ros2 run demo_arm_control gripper open
    ros2 run demo_arm_control gripper 0.02          # each finger 2 cm from the centre
"""
import sys

from demo_arm_control.trajectory_demo import FINGERS, trajectory, TrajectoryDemo
import rclpy

NAMED = {'open': 0.04, 'close': 0.0}


def main():
    rclpy.init()
    arg = sys.argv[1] if len(sys.argv) > 1 else 'open'
    width = NAMED.get(arg)
    width = float(arg) if width is None else width
    node = TrajectoryDemo()
    try:
        node.run(node.gripper, trajectory(FINGERS, [(1.0, [width, width])]), f'gripper {arg}')
    except RuntimeError as e:
        node.get_logger().error(str(e))
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
