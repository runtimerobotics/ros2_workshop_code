# clamp() lives in demo_py/util.py: plain Python, so it is tested without ROS
from demo_py.util import clamp


def test_clamp_limits():
    assert clamp(5, 0, 1) == 1
    assert clamp(-1, 0, 1) == 0
    assert clamp(0.5, 0, 1) == 0.5
