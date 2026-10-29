# Lab 10: plan with MoveIt, avoid what the camera sees

**Goal:** plan and execute in RViz, compare planners, and watch the occupancy map.

Without a simulator first:

```bash
ros2 launch demo_arm_moveit demo.launch.py
```

In RViz, MotionPlanning panel: drag the marker at the gripper, **Plan**, then **Execute**.
Try the named goal states `home` and `ready`. Switch the planner to
`pilz_industrial_motion_planner` / `LIN` and plan a small move: the tool goes straight.

Then with Gazebo and 3D vision:

```bash
ros2 launch demo_arm_moveit gazebo.launch.py
```

The RealSense point cloud fills an OctoMap: grey voxels on the table in RViz. In Gazebo,
add a box on the table (Insert a shape), wait two seconds, and plan across it: the plan
goes around something MoveIt was never told about.

```bash
ros2 service call /clear_octomap std_srvs/srv/Empty     # forget the map; it fills again
```

**Done when** you have planned around an obstacle that only the camera knows about.

**Challenge:** in `config/moveit_py.yaml` and `joint_limits.yaml`, halve the scaling
factors; plan again and compare the trajectory duration.
