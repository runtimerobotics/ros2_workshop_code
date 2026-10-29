"""
Launch arguments and substitutions.

Run:
    ros2 launch demo_launch turtles.launch.py --show-args
    ros2 launch demo_launch turtles.launch.py ns:=robot1 background_r:=200
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('ns', default_value='turtlesim1'),
        DeclareLaunchArgument('background_r', default_value='69'),
        Node(
            package='turtlesim', executable='turtlesim_node',
            namespace=LaunchConfiguration('ns'),
            parameters=[{
                'background_r': LaunchConfiguration('background_r')}]),
    ])
