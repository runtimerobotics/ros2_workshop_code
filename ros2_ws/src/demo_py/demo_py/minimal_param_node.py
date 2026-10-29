"""
Declare, read, and validate a parameter.

Run:
    ros2 run demo_py minimal_param_node --ros-args -p my_parameter:=earth
    ros2 param set /minimal_param_node my_parameter ""      # rejected: name is empty
"""
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node


class MinimalParam(Node):

    def __init__(self):
        super().__init__('minimal_param_node')
        self.declare_parameter('my_parameter', 'world')
        self.add_on_set_parameters_callback(self.on_set)
        self.timer = self.create_timer(1.0, self.tick)

    def tick(self):
        name = self.get_parameter('my_parameter').value
        self.get_logger().info(f'Hello {name}!')

    def on_set(self, params):
        for p in params:
            if p.name == 'my_parameter' and not p.value:
                return SetParametersResult(
                    successful=False, reason='name is empty')
        return SetParametersResult(successful=True)


def main():
    rclpy.init()
    try:
        rclpy.spin(MinimalParam())
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
