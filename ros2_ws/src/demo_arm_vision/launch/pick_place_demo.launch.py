"""
Start the whole pick-and-place demo with one command.

Gazebo, the controllers, MoveIt with 3D vision, the box detector, and the
pick-and-place node.

Run:
    ros2 launch demo_arm_vision pick_place_demo.launch.py
    ros2 launch demo_arm_vision pick_place_demo.launch.py use_vision:=false   # fixed box poses
    ros2 launch demo_arm_vision pick_place_demo.launch.py headless:=true rviz:=false
"""
import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction,
                            TimerAction)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

sys.path.insert(0, os.path.join(get_package_share_directory('demo_arm_moveit'), 'launch'))
import moveit_config  # noqa: E402


def pick_node(context):
    use_vision = context.launch_configurations['use_vision'] == 'true'
    share = get_package_share_directory('demo_arm_vision')
    params = os.path.join(share, 'config', 'params.yaml')
    config = moveit_config.build(python=True)
    node = Node(package='demo_arm_vision', executable='pick_and_place', output='screen',
                parameters=[config.to_dict(), params,
                            {'use_vision': use_vision, 'use_sim_time': True}])
    # give Gazebo, the controllers, and move_group time to come up
    delay = float(context.launch_configurations['start_delay'])
    return [TimerAction(period=delay, actions=[node])]


def generate_launch_description():
    moveit = get_package_share_directory('demo_arm_moveit')
    vision = get_package_share_directory('demo_arm_vision')
    use_vision = LaunchConfiguration('use_vision')
    return LaunchDescription([
        DeclareLaunchArgument('use_vision', default_value='true',
                              description='Find boxes with the camera'),
        DeclareLaunchArgument('headless', default_value='false'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('start_delay', default_value='20.0',
                              description='Seconds before picking starts'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(moveit, 'launch', 'gazebo.launch.py')),
            launch_arguments={'headless': LaunchConfiguration('headless'), 'vision': use_vision,
                              'rviz': LaunchConfiguration('rviz')}.items()),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(vision, 'launch', 'vision.launch.py')),
            condition=IfCondition(use_vision)),
        OpaqueFunction(function=pick_node),
    ])
