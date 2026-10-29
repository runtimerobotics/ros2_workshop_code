from glob import glob

from setuptools import find_packages, setup

package_name = 'demo_tf2'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # launch and config files must be listed here, or ros2 launch cannot find them
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='RUNTIME Robotics',
    maintainer_email='maintainer@example.com',
    description='tf2 in Python: static and dynamic broadcasters, a listener, and turtle following',
    license='Apache-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'static_frames = demo_tf2.static_frames:main',
            'turtle_frame_publisher = demo_tf2.turtle_frame_publisher:main',
            'frame_listener = demo_tf2.frame_listener:main',
            'turtle_follower = demo_tf2.turtle_follower:main',
        ],
    },
)
