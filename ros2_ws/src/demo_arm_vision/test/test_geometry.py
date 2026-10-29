import math

from demo_arm_vision.geometry import grasp_yaw, pixel_to_point, top_down_quaternion


def test_centre_pixel_is_on_the_optical_axis():
    assert pixel_to_point(320, 240, 0.9, 554.0, 554.0, 320, 240) == (0.0, 0.0, 0.9)


def test_pixel_offset_scales_with_depth():
    x, y, z = pixel_to_point(320 + 55.4, 240, 2.0, 554.0, 554.0, 320, 240)
    assert math.isclose(x, 0.2) and y == 0.0 and z == 2.0


def test_top_down_quaternion_is_unit():
    assert math.isclose(sum(c * c for c in top_down_quaternion(0.7)), 1.0)


def test_grasp_yaw_turns_the_wrist_least():
    assert math.isclose(grasp_yaw(0), 0.0)
    assert math.isclose(grasp_yaw(90), 0.0, abs_tol=1e-9)
    assert math.isclose(grasp_yaw(80), math.radians(-10))
    assert math.isclose(grasp_yaw(30), math.radians(30))
