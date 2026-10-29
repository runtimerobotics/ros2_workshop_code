"""Solution for 05_exercise_turtle_path.py."""
import importlib.util
import pathlib


def square_corners(x, y, side):
    return [(x, y), (x + side, y), (x + side, y + side), (x, y + side)]


if __name__ == '__main__':
    spec = importlib.util.spec_from_file_location('ex', pathlib.Path(__file__).parents[1] / '05_exercise_turtle_path.py')
    ex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ex)
    corners = square_corners(1.0, 1.0, 2.0)
    assert abs(ex.perimeter(corners) - 8.0) < 1e-9
    print('solution ok:', corners)
