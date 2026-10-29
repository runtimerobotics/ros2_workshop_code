"""Shared MoveIt configuration for the demo_arm launch files (not a launch file itself)."""
import os

from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def build(sim='none', vision=False, python=False):
    """Return the MoveIt configuration; python=True adds the MoveItPy settings."""
    description = get_package_share_directory('demo_arm_description')
    model = os.path.join(description, 'urdf', 'demo_arm.urdf.xacro')
    builder = (
        MoveItConfigsBuilder('demo_arm', package_name='demo_arm_moveit')
        .robot_description(file_path=model, mappings={'sim': sim})
        .robot_description_semantic(file_path='config/demo_arm.srdf')
        .robot_description_kinematics(file_path='config/kinematics.yaml')
        .joint_limits(file_path='config/joint_limits.yaml')
        .trajectory_execution(file_path='config/moveit_controllers.yaml')
        .planning_pipelines(pipelines=['ompl', 'pilz_industrial_motion_planner'],
                            default_planning_pipeline='ompl')
        .pilz_cartesian_limits(file_path='config/pilz_cartesian_limits.yaml')
    )
    if python:
        builder = builder.moveit_cpp(file_path='config/moveit_py.yaml')
    if vision:
        builder = builder.sensors_3d(file_path='config/realsense_octomap.yaml')
    return builder.to_moveit_configs()


# the occupancy map lives in the world frame, with 1 cm cells
OCTOMAP = {'octomap_frame': 'world', 'octomap_resolution': 0.01, 'max_range': 1.5}
