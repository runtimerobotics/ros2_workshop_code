"""
The camera side only: detect boxes and mirror them into the MoveIt planning scene.

Run (with demo_arm_moveit gazebo.launch.py running):
    ros2 launch demo_arm_vision vision.launch.py
    ros2 topic echo /detections/red
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params = os.path.join(get_package_share_directory('demo_arm_vision'), 'config', 'params.yaml')
    return LaunchDescription([
        Node(package='demo_arm_vision', executable='object_detector',
             parameters=[params, {'use_sim_time': True}]),
        Node(package='demo_arm_vision', executable='scene_updater',
             parameters=[params, {'use_sim_time': True}]),
    ])
