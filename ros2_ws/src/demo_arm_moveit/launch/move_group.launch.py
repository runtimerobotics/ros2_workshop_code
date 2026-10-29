"""
Start move_group (planning, the planning scene, execution) and RViz.

Run:
    ros2 launch demo_arm_moveit move_group.launch.py use_sim_time:=true vision:=true
Usually started by demo.launch.py or gazebo.launch.py instead.
"""
import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch_ros.actions import Node

sys.path.insert(0, os.path.dirname(__file__))
import moveit_config  # noqa: E402


def nodes(context):
    use_sim_time = context.launch_configurations['use_sim_time'] == 'true'
    vision = context.launch_configurations['vision'] == 'true'
    config = moveit_config.build(vision=vision)
    params = [config.to_dict(), {'use_sim_time': use_sim_time}]
    if vision:
        params.append(moveit_config.OCTOMAP)
    rviz = os.path.join(get_package_share_directory('demo_arm_moveit'), 'config', 'moveit.rviz')
    out = [Node(package='moveit_ros_move_group', executable='move_group', output='screen',
                parameters=params)]
    if context.launch_configurations['rviz'] == 'true':
        out.append(Node(package='rviz2', executable='rviz2', arguments=['-d', rviz], parameters=[
            config.robot_description, config.robot_description_semantic,
            config.robot_description_kinematics, config.planning_pipelines, config.joint_limits,
            {'use_sim_time': use_sim_time}]))
    return out


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('vision', default_value='false',
                              description='Octomap from the RealSense'),
        DeclareLaunchArgument('rviz', default_value='true'),
        OpaqueFunction(function=nodes),
    ])
