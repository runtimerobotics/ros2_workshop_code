"""
Change another node's parameters: turtlesim's background colour.

turtlesim reads background_r/g/b when set and redraws at once (call /clear
on older versions). This uses the same parameter services as ros2 param set.

    ros2 run demo_turtlesim background_color --ros-args -p r:=200 -p g:=86 -p b:=255
"""
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.parameter_client import AsyncParameterClient


class BackgroundColor(Node):
    def __init__(self):
        super().__init__('background_color')
        for name, value in (('r', 200), ('g', 86), ('b', 255), ('target', '/turtlesim')):
            self.declare_parameter(name, value)

    def run(self):
        target = self.get_parameter('target').value
        client = AsyncParameterClient(self, target)
        if not client.wait_for_services(timeout_sec=5.0):
            self.get_logger().error(f'{target} has no parameter services: is it running?')
            return
        params = [Parameter(f'background_{c}', value=self.get_parameter(c).value) for c in 'rgb']
        future = client.set_parameters(params)
        rclpy.spin_until_future_complete(self, future)
        ok = all(r.successful for r in future.result().results)
        values = [p.value for p in params]
        self.get_logger().info(f'{target} background set to {values}' if ok else 'rejected')


def main():
    rclpy.init()
    node = BackgroundColor()
    node.run()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
