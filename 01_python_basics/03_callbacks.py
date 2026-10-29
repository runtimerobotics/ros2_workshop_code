"""
Imports and callbacks: pass a function now, it is called later.

This is how a ROS 2 subscription works: you hand over on_message, and rclpy
calls it whenever a message arrives. The std_msgs import needs ROS sourced:
    source /opt/ros/jazzy/setup.bash && python3 03_callbacks.py
"""
import math
from std_msgs.msg import String   # from a package

def on_message(text):
    print('received:', text)

def subscribe(callback):
    # the caller decides what happens later
    for text in ['hello', 'world']:
        callback(text)

subscribe(on_message)   # pass the function, no ()

def main():
    print(math.pi)

if __name__ == '__main__':
    main()
