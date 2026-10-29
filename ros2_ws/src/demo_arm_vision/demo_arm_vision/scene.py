"""Build planning-scene messages: boxes, the table, attach and detach."""
from geometry_msgs.msg import Pose
from moveit_msgs.msg import AttachedCollisionObject, CollisionObject, PlanningScene
from shape_msgs.msg import SolidPrimitive

GRIPPER_LINKS = ['link5', 'left_finger_link', 'right_finger_link']


def box_object(name, x, y, z, size, frame='world', qx=0.0, qy=0.0, qz=0.0, qw=1.0):
    obj = CollisionObject(id=name, operation=CollisionObject.ADD)
    obj.header.frame_id = frame
    sx, sy, sz = size if isinstance(size, (list, tuple)) else (size, size, size)
    obj.primitives.append(SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[sx, sy, sz]))
    pose = Pose()
    pose.position.x, pose.position.y, pose.position.z = x, y, z
    pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w = qx, qy, qz, qw
    obj.primitive_poses.append(pose)
    return obj


def add(*objects):
    scene = PlanningScene(is_diff=True)
    scene.world.collision_objects.extend(objects)
    return scene


def attach(name, link='link5'):
    """Move a world object onto the robot: it moves with the hand and may touch the gripper."""
    scene = PlanningScene(is_diff=True)
    aco = AttachedCollisionObject(link_name=link, touch_links=GRIPPER_LINKS)
    aco.object.id = name
    aco.object.operation = CollisionObject.ADD
    scene.robot_state.attached_collision_objects.append(aco)
    scene.robot_state.is_diff = True
    return scene


def detach(name, link='link5'):
    """Take an object off the robot: it stays in the world where it was released."""
    scene = PlanningScene(is_diff=True)
    aco = AttachedCollisionObject(link_name=link)
    aco.object.id = name
    aco.object.operation = CollisionObject.REMOVE
    scene.robot_state.attached_collision_objects.append(aco)
    scene.robot_state.is_diff = True
    return scene
