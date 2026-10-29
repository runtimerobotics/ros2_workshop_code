"""Imports and callbacks: pass a function now, it is called later.

This is exactly how a ROS 2 subscription works: you hand over on_message,
and rclpy calls it whenever a message arrives.

Run: python3 03_callbacks.py
"""
import math


def on_message(text):
    print('received:', text)


def subscribe(callback):
    # the caller decides what happens later
    for text in ['hello', 'world']:
        callback(text)


def main():
    subscribe(on_message)   # pass the function itself: no ()
    # subscribe(on_message()) would call it right now, with no argument: TypeError
    print(math.pi)


if __name__ == '__main__':
    main()
