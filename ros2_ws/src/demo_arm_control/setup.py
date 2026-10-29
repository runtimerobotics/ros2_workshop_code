from glob import glob

from setuptools import find_packages, setup

package_name = 'demo_arm_control'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='RUNTIME Robotics',
    maintainer_email='maintainer@example.com',
    description='ros2_control controllers for demo_arm, mock hardware, and trajectory demos',
    license='Apache-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'trajectory_demo = demo_arm_control.trajectory_demo:main',
            'gripper = demo_arm_control.gripper:main',
        ],
    },
)
