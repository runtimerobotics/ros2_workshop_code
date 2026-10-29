"""The model expands with xacro and has the joints the rest of the workshop expects."""
import os
import subprocess
import xml.etree.ElementTree as ET

import pytest

URDF = os.path.join(os.path.dirname(__file__), '..', 'urdf', 'demo_arm.urdf.xacro')
ARM = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']
FINGERS = ['left_finger_joint', 'right_finger_joint']


def expand(*args):
    return ET.fromstring(subprocess.check_output(['xacro', URDF, *args]))


@pytest.mark.parametrize('args', [[], ['sim:=mock'], ['sim:=gazebo', 'controllers:=/tmp/c.yaml']])
def test_expands(args):
    robot = expand(*args)
    # findall: only the robot's joints, not the <joint> entries inside <ros2_control>
    joints = {j.get('name'): j.get('type') for j in robot.findall('joint')}
    assert all(joints[j] == 'revolute' for j in ARM)
    assert all(joints[j] == 'prismatic' for j in FINGERS)
    links = {link.get('name') for link in robot.findall('link')}
    assert {'tool0', 'camera_color_optical_frame', 'lidar_link', 'imu_link'} <= links


def test_ros2_control_only_in_sim():
    assert expand().find('ros2_control') is None
    plugin = expand('sim:=mock').find('ros2_control/hardware/plugin').text
    assert plugin == 'mock_components/GenericSystem'
