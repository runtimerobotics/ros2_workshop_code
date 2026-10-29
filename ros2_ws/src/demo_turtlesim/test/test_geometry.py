import math

from demo_turtlesim.draw_square import square_corners
from demo_turtlesim.go_to_goal import wrap


def test_square_corners():
    assert square_corners(1.0, 1.0, 2.0) == [(1.0, 1.0), (3.0, 1.0), (3.0, 3.0), (1.0, 3.0)]


def test_wrap_keeps_angles_in_range():
    assert math.isclose(wrap(3 * math.pi / 2), -math.pi / 2)
    assert math.isclose(wrap(-3 * math.pi / 2), math.pi / 2)
    assert wrap(0.5) == 0.5
