"""
Event handlers: spawn turtle2 when turtlesim starts; shut everything down when it exits.

Run:
    ros2 launch demo_launch events.launch.py
    (close the turtlesim window: the whole launch stops)
"""
from importlib.util import find_spec

from launch import LaunchDescription
from launch.actions import (EmitEvent, ExecuteProcess, LogInfo,
                            RegisterEventHandler)
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.events import Shutdown
from launch_ros.actions import Node

# Kilted and newer keep the turtlesim types in turtlesim_msgs; Jazzy in turtlesim
MSGS = 'turtlesim_msgs' if find_spec('turtlesim_msgs') else 'turtlesim'


def generate_launch_description():
    sim = Node(package='turtlesim', executable='turtlesim_node')
    spawn = ExecuteProcess(cmd=[
        'ros2', 'service', 'call', '/spawn', f'{MSGS}/srv/Spawn',
        "{x: 2.0, y: 2.0, name: 'turtle2'}"])
    return LaunchDescription([
        sim,
        RegisterEventHandler(OnProcessStart(
            target_action=sim, on_start=[spawn])),
        RegisterEventHandler(OnProcessExit(
            target_action=sim,
            on_exit=[LogInfo(msg='turtlesim closed'),
                     EmitEvent(event=Shutdown())])),
    ])
