"""
MoveIt with mock hardware: plan and execute in RViz, no simulator needed.

Run:
    ros2 launch demo_arm_moveit demo.launch.py
In RViz: drag the interactive marker, then Plan and Execute in the MotionPlanning panel.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    moveit = get_package_share_directory('demo_arm_moveit')
    description = get_package_share_directory('demo_arm_description')
    control = get_package_share_directory('demo_arm_control')
    model = os.path.join(description, 'urdf', 'demo_arm.urdf.xacro')
    controllers = os.path.join(control, 'config', 'controllers.yaml')
    robot_description = ParameterValue(Command(['xacro ', model, ' sim:=mock']), value_type=str)
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        Node(package='controller_manager', executable='ros2_control_node',
             parameters=[controllers]),
        Node(package='controller_manager', executable='spawner',
             arguments=['joint_state_broadcaster', 'arm_controller', 'gripper_controller']),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(moveit, 'launch', 'move_group.launch.py')),
            launch_arguments={'rviz': LaunchConfiguration('rviz')}.items()),
    ])
