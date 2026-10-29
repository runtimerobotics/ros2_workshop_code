"""
Service clients: spawn a turtle, then teleport it.

Run:
    ros2 run demo_turtlesim spawn_turtle --ros-args -p name:=turtle2 -p x:=2.0 -p y:=2.0
"""
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, TeleportAbsolute


class SpawnTurtle(Node):
    def __init__(self):
        super().__init__('spawn_turtle')
        for name, value in (('name', 'turtle2'), ('x', 2.0), ('y', 2.0), ('theta', 0.0)):
            self.declare_parameter(name, value)

    def call(self, srv_type, name, request):
        client = self.create_client(srv_type, name)
        if not client.wait_for_service(timeout_sec=5.0):
            raise RuntimeError(f'{name} is not available: is turtlesim running?')
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

    def run(self):
        p = {n: self.get_parameter(n).value for n in ('name', 'x', 'y', 'theta')}
        request = Spawn.Request(x=p['x'], y=p['y'], theta=p['theta'], name=p['name'])
        reply = self.call(Spawn, '/spawn', request)
        self.get_logger().info(f'spawned {reply.name}')
        self.call(TeleportAbsolute, f'/{reply.name}/teleport_absolute',
                  TeleportAbsolute.Request(x=p['x'] + 1.0, y=p['y'] + 1.0, theta=1.57))
        self.get_logger().info(f'teleported {reply.name} to ({p["x"] + 1.0}, {p["y"] + 1.0})')


def main():
    rclpy.init()
    node = SpawnTurtle()
    try:
        node.run()
    except RuntimeError as e:
        node.get_logger().error(str(e))
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
