from glob import glob

from setuptools import find_packages, setup

package_name = 'demo_arm_vision'

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
    description='RealSense box detection with OpenCV and pick and place with MoveItPy',
    license='Apache-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'object_detector = demo_arm_vision.object_detector:main',
            'scene_updater = demo_arm_vision.scene_updater:main',
            'pick_and_place = demo_arm_vision.pick_and_place:main',
        ],
    },
)
