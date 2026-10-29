from glob import glob

from setuptools import find_packages, setup

package_name = 'demo_py'

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
    description='Topics, services, actions, parameters, timers, and executors in Python',
    license='Apache-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'talker = demo_py.talker:main',
            'listener = demo_py.listener:main',
            'rate_talker = demo_py.rate_talker:main',
            'num_publisher = demo_py.num_publisher:main',
            'add_two_ints_server = demo_py.add_two_ints_server:main',
            'add_two_ints_client = demo_py.add_two_ints_client:main',
            'add_three_ints_server = demo_py.add_three_ints_server:main',
            'fibonacci_action_server = demo_py.fibonacci_action_server:main',
            'fibonacci_action_client = demo_py.fibonacci_action_client:main',
            'minimal_param_node = demo_py.minimal_param_node:main',
            'heartbeat = demo_py.heartbeat:main',
            'executor_demo = demo_py.executor_demo:main',
            'logging_demo = demo_py.logging_demo:main',
        ],
    },
)
