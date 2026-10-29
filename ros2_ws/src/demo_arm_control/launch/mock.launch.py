"""
ros2_control without a simulator: mock hardware copies commands straight to states.

Run:
    ros2 launch demo_arm_control mock.launch.py
    ros2 control list_controllers
    ros2 run demo_arm_control trajectory_demo
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    description = get_package_share_directory('demo_arm_description')
    control = get_package_share_directory('demo_arm_control')
    controllers = os.path.join(control, 'config', 'controllers.yaml')
    model = os.path.join(description, 'urdf', 'demo_arm.urdf.xacro')
    robot_description = ParameterValue(Command(['xacro ', model, ' sim:=mock']), value_type=str)
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        Node(package='controller_manager', executable='ros2_control_node',
             parameters=[controllers], output='screen'),
        Node(package='controller_manager', executable='spawner',
             arguments=['joint_state_broadcaster', 'arm_controller', 'gripper_controller']),
        Node(package='rviz2', executable='rviz2',
             condition=IfCondition(LaunchConfiguration('rviz')),
             arguments=['-d', os.path.join(description, 'rviz', 'display.rviz')]),
    ])
