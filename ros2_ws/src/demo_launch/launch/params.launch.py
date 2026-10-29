"""
Load parameters from a YAML file, and remap a topic into a namespace.

Run:
    ros2 launch demo_launch params.launch.py
    ros2 param get /styled/turtlesim background_b
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params = os.path.join(get_package_share_directory('demo_launch'), 'config', 'turtlesim.yaml')
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node',
             name='turtlesim', namespace='styled',
             parameters=[params]),
        # draw_circle publishes /turtle1/cmd_vel; remap it into the namespace
        Node(package='demo_turtlesim', executable='draw_circle',
             remappings=[('/turtle1/cmd_vel', '/styled/turtle1/cmd_vel')]),
    ])
