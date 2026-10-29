"""
Two turtlesims; the second copies the first through the mimic node.

Run:
    ros2 launch demo_launch mimic.launch.py
    ros2 topic pub -r 1 /turtlesim1/turtle1/cmd_vel geometry_msgs/msg/Twist \
      "{linear: {x: 2.0}, angular: {z: -1.8}}"
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', namespace='turtlesim1', name='sim'),
        Node(package='turtlesim', executable='turtlesim_node', namespace='turtlesim2', name='sim'),
        Node(package='turtlesim', executable='mimic', name='mimic', remappings=[
            ('/input/pose', '/turtlesim1/turtle1/pose'),
            ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
        ]),
    ])
