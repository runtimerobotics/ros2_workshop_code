"""
Compose launch files: include the XML and YAML files, each in its own namespace.

Run:
    ros2 launch demo_launch include.launch.py
    ros2 node list        # /from_xml/turtlesim and /from_yaml/turtlesim
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource


def generate_launch_description():
    share = get_package_share_directory('demo_launch')
    return LaunchDescription([
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(os.path.join(share, 'launch', 'turtles.launch.xml')),
            launch_arguments={'ns': 'from_xml'}.items()),
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(os.path.join(share, 'launch', 'turtles.launch.yaml')),
            launch_arguments={'ns': 'from_yaml'}.items()),
    ])
