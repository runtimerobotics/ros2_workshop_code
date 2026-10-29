from glob import glob

from setuptools import find_packages, setup

package_name = 'demo_launch'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.*')),   # .py, .xml, and .yaml
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='RUNTIME Robotics',
    maintainer_email='maintainer@example.com',
    description='Launch files in Python, XML, and YAML',
    license='Apache-2.0',
    tests_require=['pytest'],
)
