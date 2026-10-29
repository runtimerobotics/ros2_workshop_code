# Lab 12: pick and place

**Goal:** a complete, collision-aware manipulation task, first with fixed poses, then with vision.

```bash
ros2 launch demo_arm_vision pick_place_demo.launch.py use_vision:=false
ros2 launch demo_arm_vision pick_place_demo.launch.py                       # with the camera
```

Read `pick_and_place.py` step by step, and match each log line to the robot:

| Log line | Planner | Planning scene |
|---|---|---|
| `pre-grasp` | OMPL (free motion) | the box is a world object |
| `approach (straight down)` | Pilz LIN | |
| `close gripper` | named state `close` | box attached to `link5`; it may touch the fingers |
| `lift`, `over the tray`, `lower` | LIN, OMPL, LIN | the box moves with the hand |
| `open gripper`, `retreat` | named state, LIN | box detached: a world object again |

Gazebo locks the box to the palm while it is held (`/demo_arm/red_box/attach`);
friction grasps of small boxes slip in simulation.

**Done when** both boxes end up in the green tray, and you can say when the box is a
world object and when it is attached.

**Challenge:** sort by colour: give each colour its own place pose in `params.yaml`
and change `pick_and_place()` to use it.
