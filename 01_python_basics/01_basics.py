"""Python basics: values, lists, dictionaries, f-strings, loops, if, functions.

Run: python3 01_basics.py
"""

speed = 0.5                    # float
name = 'turtle1'               # string
joints = ['joint1', 'joint2']  # list
limits = {'max_speed': 1.0}    # dictionary

print(f'{name} moves at {speed} m/s')

for joint in joints:
    print(joint)

if speed > limits['max_speed']:
    print('too fast')
else:
    print('ok')


def clamp(value, low, high):
    """Keep value between low and high."""
    return max(low, min(value, high))


print(f'clamp(1.7, 0.0, 1.0) -> {clamp(1.7, 0.0, 1.0)}')
