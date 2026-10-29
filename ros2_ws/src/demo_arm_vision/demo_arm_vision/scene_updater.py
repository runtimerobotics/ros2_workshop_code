"""
Keep the MoveIt planning scene in step with what the camera sees.

Adds the table once, then moves each detected box to its latest detected pose. Boxes the
robot is holding are left alone: while attached, they move with the hand.

Run:
    ros2 run demo_arm_vision scene_updater
"""
from demo_arm_vision import scene
from geometry_msgs.msg import PoseStamped
from moveit_msgs.msg import PlanningSceneComponents
from moveit_msgs.srv import ApplyPlanningScene, GetPlanningScene
import rclpy
from rclpy.node import Node


class SceneUpdater(Node):

    def __init__(self):
        super().__init__('scene_updater')
        self.box_size = self.declare_parameter('box_size', 0.04).value
        self.table = self.declare_parameter('table', [0.40, 0.0, 0.09, 0.50, 0.60, 0.02]).value
        colors = self.declare_parameter('colors', ['red', 'blue']).value
        self.apply = self.create_client(ApplyPlanningScene, '/apply_planning_scene')
        self.get = self.create_client(GetPlanningScene, '/get_planning_scene')
        self.latest = {}
        for c in colors:
            self.create_subscription(PoseStamped, f'/detections/{c}',
                                     lambda m, c=c: self.latest.update({c: m}), 10)
        self.table_added = False
        self.attached = set()
        self.create_timer(1.0, self.update)

    def update(self):
        if not self.apply.service_is_ready():
            self.get_logger().info('waiting for move_group...', throttle_duration_sec=5.0)
            return
        objects = []
        if not self.table_added:
            x, y, z, sx, sy, sz = self.table
            objects.append(scene.box_object('table', x, y, z, [sx, sy, sz]))
            self.table_added = True
        if self.get.service_is_ready():
            req = GetPlanningScene.Request()
            req.components.components = PlanningSceneComponents.ROBOT_STATE_ATTACHED_OBJECTS
            self.get.call_async(req).add_done_callback(self.on_scene)
        for color, pose in self.latest.items():
            name = f'{color}_box'
            if name in self.attached:
                continue
            p, q = pose.pose.position, pose.pose.orientation
            objects.append(scene.box_object(name, p.x, p.y, p.z, self.box_size,
                                            qx=q.x, qy=q.y, qz=q.z, qw=q.w))
        if objects:
            self.apply.call_async(ApplyPlanningScene.Request(scene=scene.add(*objects)))

    def on_scene(self, future):
        held = future.result().scene.robot_state.attached_collision_objects
        self.attached = {a.object.id for a in held}


def main():
    rclpy.init()
    try:
        rclpy.spin(SceneUpdater())
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
