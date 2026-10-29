# Labs

One page per hands-on block in the slides. Each lab lists its goal, the commands, what
"done" looks like, and a challenge. Build the workspace first (see the main README).

| # | Lab | Day | Packages |
|---|---|---|---|
| 0 | [Baseline: is this machine ready?](00_baseline.md) | setup | `setup/` |
| 1 | [Inspect a running graph](01_inspect_graph.md) | 1 | turtlesim |
| 2 | [Command the turtle](02_command_turtle.md) | 1 | `demo_turtlesim` |
| 3 | [Write and run your own nodes](03_nodes.md) | 1 | `demo_py`, `demo_cpp`, `demo_interfaces` |
| 4 | [Request and goal: services and actions](04_services_actions.md) | 1 | `demo_py`, `demo_turtlesim` |
| 5 | [One-command startup](05_launch.md) | 1 | `demo_py`, `demo_launch` |
| 6 | [Debug the frame tree](06_tf2.md) | 2 | `demo_tf2` |
| 7 | [Model the arm](07_urdf.md) | 2 | `demo_arm_description` |
| 8 | [Spawn the arm in Gazebo and read every sensor](08_gazebo_sensors.md) | 2 | `demo_arm_gazebo` |
| 9 | [Drive the arm with ros2_control](09_ros2_control.md) | 3 | `demo_arm_control` |
| 10 | [Plan with MoveIt, avoid what the camera sees](10_moveit.md) | 3 | `demo_arm_moveit` |
| 11 | [Find the boxes with OpenCV](11_vision.md) | 3 | `demo_arm_vision` |
| 12 | [Pick and place](12_pick_and_place.md) | 3 | `demo_arm_vision` |
| 13 | [Capstone](13_capstone.md) | 3 | everything |

Every terminal needs ROS and the workspace sourced:

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_workshop_code/ros2_ws/install/setup.bash
```
