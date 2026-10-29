"""
Pick coloured boxes and place them in the tray, with MoveIt's Python API (MoveItPy).

For each box:
    1. find it: a camera detection (use_vision:=true) or a fixed pose from params.yaml
    2. add it to the planning scene, open the gripper
    3. plan to a pre-grasp pose above it (OMPL)
    4. move straight down (Pilz LIN)
    5. attach it to the hand: in MoveIt and in Gazebo; close the gripper
    6. lift straight up, move over the tray, lower straight down
    7. detach it, open the gripper, retreat, and go home

Run (with the simulation and MoveIt running):
    ros2 launch demo_arm_vision pick_place_demo.launch.py
    ros2 launch demo_arm_vision pick_place_demo.launch.py use_vision:=false
"""
import math
import os
import threading
import time

from demo_arm_vision import scene
from demo_arm_vision.geometry import top_down_quaternion
from geometry_msgs.msg import PoseStamped
from moveit.planning import MoveItPy, PlanRequestParameters
from moveit_msgs.srv import ApplyPlanningScene
import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import Empty


class StepFailed(RuntimeError):

    pass


class Helper(Node):
    """The rclpy side of the demo: parameters, detections, the scene service, Gazebo topics."""

    def __init__(self):
        super().__init__('pick_and_place')
        p = self.declare_parameter
        self.use_vision = p('use_vision', True).value
        self.order = p('pick_order', ['red', 'blue']).value
        xy = p('fixed_positions', [0.36, 0.10, 0.48, -0.04]).value
        self.fixed = {c: (xy[2 * i], xy[2 * i + 1]) for i, c in enumerate(self.order)}
        self.table_height = p('table_height', 0.10).value
        self.box = p('box_size', 0.04).value
        self.approach = p('approach', 0.08).value
        self.place_xy = p('place', [0.28, -0.20]).value
        self.timeout = p('detection_timeout', 10.0).value
        self.detections = {}
        for c in self.order:
            self.create_subscription(PoseStamped, f'/detections/{c}', self.collector(c), 10)
        self.apply = self.create_client(ApplyPlanningScene, '/apply_planning_scene')
        self.gz = {(c, a): self.create_publisher(Empty, f'/demo_arm/{c}_box/{a}', 1)
                   for c in self.order for a in ('attach', 'detach')}

    def collector(self, color):
        return lambda msg: self.detections.setdefault(color, []).append(msg)

    def apply_scene(self, msg):
        if not self.apply.wait_for_service(timeout_sec=5.0):
            raise StepFailed('/apply_planning_scene not available: is move_group running?')
        done = threading.Event()
        future = self.apply.call_async(ApplyPlanningScene.Request(scene=msg))
        future.add_done_callback(lambda f: done.set())
        done.wait(5.0)

    def locate(self, color):
        """Box centre (x, y, z) and yaw in world."""
        if not self.use_vision:
            x, y = self.fixed[color]
            return x, y, self.table_height + self.box / 2, 0.0
        self.detections[color] = []
        deadline = time.time() + self.timeout
        while time.time() < deadline and len(self.detections[color]) < 5:
            time.sleep(0.1)
        seen = self.detections[color][-5:]
        if not seen:
            raise StepFailed(f'no {color} box seen in {self.timeout:.0f} s')
        med = lambda v: sorted(v)[len(v) // 2]  # noqa: E731  (median: ignores one bad frame)
        x = med([d.pose.position.x for d in seen])
        y = med([d.pose.position.y for d in seen])
        z = med([d.pose.position.z for d in seen])
        yaw = med([2 * math.atan2(d.pose.orientation.z, d.pose.orientation.w) for d in seen])
        return x, y, z, yaw

    def gazebo(self, color, action):
        self.gz[(color, action)].publish(Empty())


class PickAndPlace:

    def __init__(self, helper):
        self.h = helper
        self.log = helper.get_logger()
        self.moveit = MoveItPy(node_name='moveit_py')
        self.arm = self.moveit.get_planning_component('arm')
        self.gripper = self.moveit.get_planning_component('gripper')
        self.lin = PlanRequestParameters(self.moveit, 'pilz_lin')

    def tool_pose(self, x, y, z, yaw):
        pose = PoseStamped()
        pose.header.frame_id = 'world'
        pose.pose.position.x, pose.pose.position.y, pose.pose.position.z = x, y, z
        o = pose.pose.orientation
        o.x, o.y, o.z, o.w = top_down_quaternion(yaw)
        return pose

    def run(self, component, what, straight=False, **goal):
        component.set_start_state_to_current_state()
        component.set_goal_state(**goal)
        plan = component.plan(single_plan_parameters=self.lin) if straight else component.plan()
        if not plan:
            raise StepFailed(f'{what}: no plan found')
        status = self.moveit.execute(plan.trajectory, controllers=[])
        if not status:
            raise StepFailed(f'{what}: execution {status.status}')
        self.log.info(f'{what}: done')

    def move_arm(self, what, x, y, z, yaw, straight=False):
        goal = self.tool_pose(x, y, z, yaw)
        self.run(self.arm, what, straight, pose_stamped_msg=goal, pose_link='tool0')

    def pick_and_place(self, color, slot):
        h, name = self.h, f'{color}_box'
        x, y, z, yaw = h.locate(color)
        self.log.info(f'{color} box at ({x:.3f}, {y:.3f}, {z:.3f}), yaw {math.degrees(yaw):.0f}°')
        box = scene.box_object(name, x, y, z, h.box, qz=math.sin(yaw / 2), qw=math.cos(yaw / 2))
        h.apply_scene(scene.add(box))
        grasp_z = z + 0.005   # tool0 a little above the box centre: finger tips clear the table
        self.run(self.gripper, 'open gripper', configuration_name='open')
        self.move_arm('pre-grasp', x, y, grasp_z + h.approach, yaw)
        self.move_arm('approach (straight down)', x, y, grasp_z, yaw, straight=True)
        h.apply_scene(scene.attach(name))
        h.gazebo(color, 'attach')
        self.run(self.gripper, 'close gripper', configuration_name='close')
        self.move_arm('lift (straight up)', x, y, grasp_z + h.approach, yaw, straight=True)
        # side by side in the tray, 5 cm apart along x
        px, py = h.place_xy[0] + (slot - (len(h.order) - 1) / 2) * 0.05, h.place_xy[1]
        place_z = h.table_height + h.box / 2 + 0.01   # release 1 cm above the tray floor
        self.move_arm('over the tray', px, py, place_z + h.approach, 0.0)
        self.move_arm('lower (straight down)', px, py, place_z, 0.0, straight=True)
        h.gazebo(color, 'detach')
        h.apply_scene(scene.detach(name))
        self.run(self.gripper, 'open gripper', configuration_name='open')
        self.move_arm('retreat (straight up)', px, py, place_z + h.approach, 0.0, straight=True)

    def wait_for_controllers(self, tries=10):
        # MoveItPy's controller action clients connect a moment after start-up;
        # until then every execution is ABORTED, so retry the first moves
        for attempt in range(tries):
            try:
                self.run(self.arm, 'home', configuration_name='home')
                self.run(self.gripper, 'open gripper', configuration_name='open')
                return
            except StepFailed as e:
                if attempt == tries - 1:
                    raise
                self.log.warning(f'{e}; controllers not ready, retrying')
                time.sleep(1.0)

    def main(self):
        self.wait_for_controllers()
        skipped = []
        for slot, color in enumerate(self.h.order):
            try:
                self.pick_and_place(color, slot)
            except StepFailed as e:
                self.log.error(f'{color} box skipped: {e}')
                skipped.append(color)
        self.run(self.arm, 'home', configuration_name='home')
        if skipped:
            self.log.error(f'pick and place incomplete: skipped {", ".join(skipped)}')
        else:
            self.log.info('pick and place finished')


def main():
    rclpy.init()
    helper = Helper()
    executor = MultiThreadedExecutor()
    executor.add_node(helper)
    threading.Thread(target=executor.spin, daemon=True).start()
    demo = PickAndPlace(helper)
    try:
        demo.main()
    except StepFailed as e:
        helper.get_logger().error(str(e))
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    demo.moveit.shutdown()
    rclpy.shutdown()
    # MoveItPy can crash while Python tears it down (a known MoveItPy issue); all work is
    # done by now, so leave directly with a clean exit code.
    os._exit(0)


if __name__ == '__main__':
    main()
