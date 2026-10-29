"""
turtle2 chases turtle1, steering from the transform turtle2 → turtle1.

Started by follow.launch.py, which also spawns turtle2 and runs both frame publishers.
"""
import math

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from turtlesim.srv import Spawn


class TurtleFollower(Node):
    def __init__(self):
        super().__init__('turtle_follower')
        self.leader = self.declare_parameter('leader', 'turtle1').value
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.spawner = self.create_client(Spawn, '/spawn')
        self.spawned = False
        self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        if not self.spawned:
            if self.spawner.service_is_ready():
                self.spawner.call_async(Spawn.Request(x=2.0, y=2.0, theta=0.0, name='turtle2'))
                self.spawned = True
            return
        try:
            # where is the leader, seen from turtle2?
            t = self.buffer.lookup_transform('turtle2', self.leader, Time())
        except TransformException:
            return
        x, y = t.transform.translation.x, t.transform.translation.y
        cmd = Twist()
        if math.hypot(x, y) > 0.6:     # keep a little distance
            cmd.linear.x = 0.8 * math.hypot(x, y)
            cmd.angular.z = 3.0 * math.atan2(y, x)
        self.pub.publish(cmd)


def main():
    rclpy.init()
    try:
        rclpy.spin(TurtleFollower())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
