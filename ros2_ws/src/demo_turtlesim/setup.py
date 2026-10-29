from glob import glob

from setuptools import find_packages, setup

package_name = 'demo_turtlesim'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # launch and config files must be listed here, or ros2 launch cannot find them
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='RUNTIME Robotics',
    maintainer_email='maintainer@example.com',
    description='Turtlesim labs in Python: drive, draw, spawn, rotate, and recolour',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'draw_circle = demo_turtlesim.draw_circle:main',
            'draw_square = demo_turtlesim.draw_square:main',
            'go_to_goal = demo_turtlesim.go_to_goal:main',
            'pose_monitor = demo_turtlesim.pose_monitor:main',
            'spawn_turtle = demo_turtlesim.spawn_turtle:main',
            'rotate_turtle = demo_turtlesim.rotate_turtle:main',
            'background_color = demo_turtlesim.background_color:main',
        ],
    },
)
