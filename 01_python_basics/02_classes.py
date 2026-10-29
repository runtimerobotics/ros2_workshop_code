"""Classes and objects: attributes, methods, inheritance, super().

Run: python3 02_classes.py
"""


class Robot:
    def __init__(self, name):
        self.name = name        # attribute
        self.speed = 0.0

    def drive(self, speed):     # method
        self.speed = speed
        print(f'{self.name}: {speed} m/s')


class Rover(Robot):             # inherits Robot
    def __init__(self):
        super().__init__('rover')


r = Rover()
r.drive(0.3)
