"""
Log at every severity, and throttle a fast message to once a second.

Run:
    ros2 run demo_py logging_demo
    ros2 run demo_py logging_demo --ros-args --log-level debug     # shows the debug line too
    ros2 run rqt_console rqt_console                               # filter and colour them
"""
import rclpy
from rclpy.node import Node


class LoggingDemo(Node):

    def __init__(self):
        super().__init__('logging_demo')
        self.started = False
        self.create_timer(0.05, self.on_timer)   # 20 times a second

    def on_timer(self):
        log = self.get_logger()
        if not self.started:
            self.started = True
            log.debug('raw scan received')
            log.info('robot ready')
            log.warning('battery below 20%')
            log.error('lidar timeout')
            log.fatal('motor driver lost')
        log.info('tick', throttle_duration_sec=1.0)


def main():
    rclpy.init()
    try:
        rclpy.spin(LoggingDemo())
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
