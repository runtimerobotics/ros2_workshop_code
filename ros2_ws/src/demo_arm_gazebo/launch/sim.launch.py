"""
Gazebo Harmonic with demo_arm on a table: sensors, controllers, and the ROS bridge.

Run:
    ros2 launch demo_arm_gazebo sim.launch.py
    ros2 launch demo_arm_gazebo sim.launch.py headless:=true      # no Gazebo window
    ros2 launch demo_arm_gazebo sim.launch.py rviz:=true          # also RViz with the sensors

Then, in another terminal:
    ros2 control list_controllers
    ros2 run demo_arm_control trajectory_demo
    ros2 topic hz /camera/camera/color/image_raw
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (AppendEnvironmentVariable, DeclareLaunchArgument, ExecuteProcess,
                            IncludeLaunchDescription, RegisterEventHandler)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

BOXES = ['red_box', 'blue_box']   # objects the gripper can lock onto (DetachableJoint)


def generate_launch_description():
    gazebo = get_package_share_directory('demo_arm_gazebo')
    description = get_package_share_directory('demo_arm_description')
    control = get_package_share_directory('demo_arm_control')
    model = os.path.join(description, 'urdf', 'demo_arm.urdf.xacro')
    controllers = os.path.join(control, 'config', 'controllers.yaml')
    headless = LaunchConfiguration('headless')

    robot_description = ParameterValue(Command([
        'xacro ', model, ' sim:=gazebo controllers:=', controllers,
        ' attachables:="', ' '.join(BOXES), '"']), value_type=str)

    # -r: start running; -s --headless-rendering: server only, sensors still render
    gz_args = PythonExpression([
        "'-r -v 2 ' + ('-s --headless-rendering ' if '", headless, "' == 'true' else '') + '",
        LaunchConfiguration('world'), "'"])
    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': gz_args, 'on_exit_shutdown': 'true'}.items())

    spawn = Node(package='ros_gz_sim', executable='create', output='screen',
                 arguments=['-topic', 'robot_description', '-name', 'demo_arm'])

    # Gazebo attaches every DetachableJoint at start: release the boxes once the arm exists.
    # Repeated for a few seconds because the plugin may not listen yet; detaching twice is fine.
    release = '; '.join(f'gz topic -t /demo_arm/{b}/detach -m gz.msgs.Empty -p " "' for b in BOXES)
    detach = ExecuteProcess(
        cmd=['bash', '-c', f'for i in 1 2 3 4 5 6; do {release}; sleep 1; done'])
    spawners = Node(package='controller_manager', executable='spawner',
                    arguments=['joint_state_broadcaster', 'arm_controller', 'gripper_controller'])

    realsense = get_package_share_directory('realsense2_description')
    return LaunchDescription([
        DeclareLaunchArgument('world', default_value=os.path.join(gazebo, 'worlds', 'table.sdf')),
        DeclareLaunchArgument('headless', default_value='false',
                              description='Run Gazebo without a window'),
        DeclareLaunchArgument('rviz', default_value='false',
                              description='Start RViz with the sensor displays'),
        # lets Gazebo find package:// meshes, such as the RealSense model
        AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.dirname(realsense)),
        AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.dirname(description)),
        gz,
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description, 'use_sim_time': True}]),
        spawn,
        RegisterEventHandler(OnProcessExit(target_action=spawn, on_exit=[detach, spawners])),
        Node(package='ros_gz_bridge', executable='parameter_bridge', name='bridge',
             parameters=[{'config_file': os.path.join(gazebo, 'config', 'bridge.yaml'),
                          'use_sim_time': True}]),
        Node(package='demo_arm_gazebo', executable='points_frame_fix.py',
             parameters=[{'use_sim_time': True}]),
        Node(package='rviz2', executable='rviz2',
             condition=IfCondition(LaunchConfiguration('rviz')),
             arguments=['-d', os.path.join(gazebo, 'rviz', 'sensors.rviz')],
             parameters=[{'use_sim_time': True}]),
    ])
