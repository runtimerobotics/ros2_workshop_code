"""Exercise: plan a square path without ROS.

Fill in square_corners() so it returns the four corners of a square,
starting at (x, y) and going counter-clockwise. Then run the tests:

    python3 05_exercise_turtle_path.py

The ROS 2 version of this exercise (demo_turtlesim draw_square) drives
the real turtle along the same corners.
"""


def square_corners(x, y, side):
    # TODO: return [(x, y), ...] with four (x, y) tuples
    raise NotImplementedError


def perimeter(points):
    total = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
        total += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return total


if __name__ == '__main__':
    corners = square_corners(1.0, 1.0, 2.0)
    assert corners[0] == (1.0, 1.0), 'start at (x, y)'
    assert len(corners) == 4, 'four corners'
    assert abs(perimeter(corners) - 8.0) < 1e-9, 'perimeter of a 2 m square is 8 m'
    print('all checks passed:', corners)
