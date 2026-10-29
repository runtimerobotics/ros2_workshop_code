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
