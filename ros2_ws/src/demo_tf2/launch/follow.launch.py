"""
turtle2 follows turtle1 using tf2 (replaces the turtle_tf2_py demo).

Run:
    ros2 launch demo_tf2 follow.launch.py
    ros2 run turtlesim turtle_teleop_key        # drive turtle1, turtle2 follows
    ros2 run tf2_tools view_frames
    ros2 run tf2_ros tf2_echo turtle2 turtle1
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(package='demo_tf2', executable='turtle_frame_publisher', name='broadcaster1',
             parameters=[{'turtlename': 'turtle1'}]),
        Node(package='demo_tf2', executable='turtle_frame_publisher', name='broadcaster2',
             parameters=[{'turtlename': 'turtle2'}]),
        Node(package='demo_tf2', executable='turtle_follower', output='screen'),
    ])
