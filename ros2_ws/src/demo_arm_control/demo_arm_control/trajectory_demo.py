"""
Send joint trajectories straight to the controllers, with no planner.

The arm goes through three poses in one trajectory, the gripper closes and opens.
This is what MoveIt does at the end of planning: a FollowJointTrajectory goal.

Run:
    ros2 launch demo_arm_gazebo sim.launch.py      (or demo_arm_control mock.launch.py)
    ros2 run demo_arm_control trajectory_demo
"""
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

ARM = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']
FINGERS = ['left_finger_joint', 'right_finger_joint']
POSES = [  # seconds from start, joint positions in rad
    (3.0, [0.0, -0.4, 1.9, 1.0, 0.0]),     # home
    (6.0, [0.6, 0.5, 0.9, 1.4, 0.6]),      # over the table, left
    (9.0, [-0.5, 0.4, 1.1, 1.3, -0.5]),    # over the table, right
    (12.0, [0.0, -0.4, 1.9, 1.0, 0.0]),    # home again
]


def trajectory(joints, points):
    traj = JointTrajectory(joint_names=joints)
    for t, q in points:
        traj.points.append(JointTrajectoryPoint(
            positions=q, time_from_start=Duration(sec=int(t), nanosec=int(t % 1 * 1e9))))
    return traj


class TrajectoryDemo(Node):

    def __init__(self):
        super().__init__('trajectory_demo')
        self.arm = ActionClient(
            self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')
        self.gripper = ActionClient(
            self, FollowJointTrajectory, '/gripper_controller/follow_joint_trajectory')

    def run(self, client, traj, what):
        if not client.wait_for_server(timeout_sec=10.0):
            raise RuntimeError(f'{client._action_name} not available: are the controllers active?')
        goal = client.send_goal_async(FollowJointTrajectory.Goal(trajectory=traj))
        rclpy.spin_until_future_complete(self, goal)
        if not goal.result().accepted:
            raise RuntimeError(f'{what}: goal rejected')
        result = goal.result().get_result_async()
        rclpy.spin_until_future_complete(self, result)
        code = result.result().result.error_code
        self.get_logger().info(f'{what}: {"done" if code == 0 else f"error {code}"}')

    def main(self):
        self.run(self.arm, trajectory(ARM, POSES), 'arm through 4 poses')
        self.run(self.gripper, trajectory(FINGERS, [(1.0, [0.0, 0.0])]), 'gripper close')
        self.run(self.gripper, trajectory(FINGERS, [(1.0, [0.04, 0.04])]), 'gripper open')


def main():
    rclpy.init()
    node = TrajectoryDemo()
    try:
        node.main()
    except RuntimeError as e:
        node.get_logger().error(str(e))
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
