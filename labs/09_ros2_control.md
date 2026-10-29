# Lab 9: drive the arm with ros2_control

**Goal:** see the controllers, their interfaces, and send trajectories without a planner.

```bash
ros2 launch demo_arm_gazebo sim.launch.py          # or: ros2 launch demo_arm_control mock.launch.py

ros2 control list_hardware_components
ros2 control list_hardware_interfaces              # position commands, position + velocity states
ros2 control list_controllers                      # joint_state_broadcaster, arm_controller, gripper_controller
ros2 action info /arm_controller/follow_joint_trajectory

ros2 run demo_arm_control trajectory_demo          # four poses, then the gripper
ros2 run demo_arm_control gripper close
ros2 run demo_arm_control gripper open
ros2 topic echo /arm_controller/controller_state   # reference vs feedback while moving
```

Two controllers cannot claim the same joint:

```bash
ros2 control set_controller_state arm_controller inactive
ros2 run demo_arm_control trajectory_demo          # goal rejected: the controller is inactive
ros2 control set_controller_state arm_controller active
```

**Done when** the trajectory demo runs and you can explain what `trajectory` and
`goal` tolerances in `controllers.yaml` do.

**Challenge:** add a fifth pose to `POSES` in `trajectory_demo.py` that puts the gripper
over the tray at (0.28, -0.20).
