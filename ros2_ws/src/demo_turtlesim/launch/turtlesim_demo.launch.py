"""
turtlesim + a demo node + the wall monitor, in one command.

Run:
    ros2 launch demo_turtlesim turtlesim_demo.launch.py                 # draws a circle
    ros2 launch demo_turtlesim turtlesim_demo.launch.py demo:=draw_square
    ros2 launch demo_turtlesim turtlesim_demo.launch.py demo:=go_to_goal
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('demo_turtlesim')
    params = os.path.join(share, 'config', 'turtlesim.yaml')
    return LaunchDescription([
        DeclareLaunchArgument('demo', default_value='draw_circle',
                              description='draw_circle, draw_square, or go_to_goal'),
        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim',
             parameters=[params]),
        Node(package='demo_turtlesim', executable=LaunchConfiguration('demo'),
             parameters=[params], output='screen'),
        Node(package='demo_turtlesim', executable='pose_monitor',
             parameters=[params], output='screen'),
    ])
