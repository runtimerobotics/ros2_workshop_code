"""
One command, two nodes, settings from a YAML file (the one-command startup lab).

Run:
    ros2 launch demo_py demo.launch.py
    ros2 launch demo_py demo.launch.py params:=/path/to/other.yaml
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('demo_py')
    default_params = os.path.join(share, 'config', 'params.yaml')
    params = LaunchConfiguration('params')
    return LaunchDescription([
        DeclareLaunchArgument('params', default_value=default_params,
                              description='YAML parameter file'),
        Node(package='demo_py', executable='rate_talker', parameters=[params], output='screen'),
        Node(package='demo_py', executable='listener', output='screen'),
    ])
