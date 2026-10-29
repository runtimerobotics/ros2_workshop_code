"""
Ask the tf2 buffer for a transform once a second; handle "not yet" gracefully.

Run:
    ros2 run demo_tf2 frame_listener --ros-args -p target:=world -p source:=turtle1
"""
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):
    def __init__(self):
        super().__init__('frame_listener')
        self.target = self.declare_parameter('target', 'world').value
        self.source = self.declare_parameter('source', 'turtle1').value
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        try:
            t = self.buffer.lookup_transform(self.target, self.source, Time())
        except TransformException as ex:
            self.get_logger().info(f'not yet: {ex}')
            return
        p = t.transform.translation
        self.get_logger().info(f'{self.source} at x={p.x:.2f} y={p.y:.2f}')


def main():
    rclpy.init()
    try:
        rclpy.spin(FrameListener())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
