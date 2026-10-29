"""
Show the arm in RViz and move its joints with sliders.

Run:
    ros2 launch demo_arm_description display.launch.py
    ros2 launch demo_arm_description display.launch.py gui:=false     # no slider window
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    share = get_package_share_directory('demo_arm_description')
    model = os.path.join(share, 'urdf', 'demo_arm.urdf.xacro')
    robot_description = ParameterValue(Command(['xacro ', model]), value_type=str)
    gui = LaunchConfiguration('gui')
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true', description='Joint slider window'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             condition=IfCondition(gui)),
        Node(package='joint_state_publisher', executable='joint_state_publisher',
             condition=UnlessCondition(gui)),
        Node(package='rviz2', executable='rviz2',
             arguments=['-d', os.path.join(share, 'rviz', 'display.rviz')]),
    ])
