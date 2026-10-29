"""
Self-check: predict the output before you run it.

1. How many times is "battery ..." printed?
2. What is the last line?
3. Change one character so the robot stops at 30% instead of 20%.

Run: python3 04_self_check.py      (answers: solutions/04_self_check.md)
"""

class Robot:
    def __init__(self, name, on_change):
        self.name = name
        self.battery = 100
        self.on_change = on_change

    def drive(self):
        if self.battery <= 20:
            print('battery low')
            return
        self.battery -= 10
        self.on_change(self.battery)

r = Robot('rover', lambda b: print(f'battery {b}%'))
for _ in range(10):
    r.drive()
