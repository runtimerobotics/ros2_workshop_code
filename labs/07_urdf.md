# Lab 7: model the arm

**Goal:** read a real URDF, move its joints, and check it.

```bash
ros2 launch demo_arm_description display.launch.py      # RViz + joint sliders
```

Then look inside:

```bash
cd ros2_ws/src/demo_arm_description/urdf
xacro demo_arm.urdf.xacro > /tmp/demo_arm.urdf
check_urdf /tmp/demo_arm.urdf                 # the tree: world → base_link → link1 → ...
urdf_to_graphviz /tmp/demo_arm.urdf demo_arm  # a PDF of links and joints
```

| File | Holds |
|---|---|
| `demo_arm.xacro` | links, joints, limits, inertia |
| `macros.xacro` | `box_link`: visual, collision, and inertia from one size |
| `sensors.xacro` | camera stand, RealSense D435, lidar, IMU frames |
| `demo_arm.ros2_control.xacro` | which joints are commanded, and their start pose |
| `gazebo.xacro` | what each sensor measures in Gazebo |

**Done when** you can move `joint2` in the slider window and name the links that move with it.

**Challenge:** make the forearm (`link3`) 5 cm longer. What else must change? (Its joint
origin, and the reach in the pick-and-place poses.) Rebuild, check, view.

## Part 2 (Day 3 morning): joint space and task space

**Goal:** see how joint angles (joint space) decide where the tool is (task space).

```bash
ros2 launch demo_arm_description display.launch.py
ros2 topic echo /joint_states
ros2 run tf2_ros tf2_echo base_link tool0          # the tool pose, live
```

Move one slider at a time and write down the tool position for three configurations.
Then publish a pose yourself (close the slider window first: only one publisher may own `/joint_states`):

```bash
ros2 topic pub --once /joint_states sensor_msgs/msg/JointState \
  "{name: [joint1, joint2, joint3, joint4, joint5, left_finger_joint, right_finger_joint],
    position: [0.0, 1.6, 0.0, 0.0, 0.0, 0.02, 0.02]}"
```

**Done when** you can say why the tool cannot get further than about 0.7 m from the
shoulder (the arm is stretched out: a singular configuration), and why it cannot point the
tool in every direction at one spot (five joints, not six).

