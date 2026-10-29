"""
Launch describes a system: one node in a namespace, with a parameter.

Run:
    ros2 launch demo_launch namespace.launch.py
    ros2 node list                  # /demo/turtlesim
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            namespace='demo',
            parameters=[{'background_r': 20}],
        )
    ])
