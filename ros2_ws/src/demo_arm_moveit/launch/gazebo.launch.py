"""
Gazebo + controllers + MoveIt with 3D vision: the full stack for pick and place.

Run:
    ros2 launch demo_arm_moveit gazebo.launch.py
    ros2 launch demo_arm_moveit gazebo.launch.py headless:=true vision:=false
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    sim = os.path.join(get_package_share_directory('demo_arm_gazebo'), 'launch', 'sim.launch.py')
    moveit = get_package_share_directory('demo_arm_moveit')
    move_group = os.path.join(moveit, 'launch', 'move_group.launch.py')
    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='false'),
        DeclareLaunchArgument('vision', default_value='true',
                              description='Octomap from the RealSense'),
        DeclareLaunchArgument('rviz', default_value='true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sim),
            launch_arguments={'headless': LaunchConfiguration('headless')}.items()),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(move_group),
            launch_arguments={'use_sim_time': 'true', 'vision': LaunchConfiguration('vision'),
                              'rviz': LaunchConfiguration('rviz')}.items()),
    ])
