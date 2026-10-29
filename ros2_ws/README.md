# Run every example

The command for each node and launch file in the workspace, in workshop order, with the
output you should see. **T1**, **T2**, and **T3** are separate terminals. Stop a running node with
`Ctrl+C`.

## Before you start

Build once, and after every change to a C++ file, `package.xml`, or `setup.py`:

```bash
cd ~/ros2_workshop_code/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src -y --ignore-src
colcon build --symlink-install
```

Source the workspace in **every new terminal** (or add both lines to `~/.bashrc`):

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_workshop_code/ros2_ws/install/setup.bash
```

To check everything at once, run `bash scripts/smoke_test.sh`. It runs each example below
briefly and prints ✓ or ✗ for each one. Set `SKIP_SIM=1` to skip the 3-minute Gazebo run.

Contents:
[demo_py](#demo_py-topics-services-actions-parameters) ·
[demo_cpp](#demo_cpp-the-same-in-c) ·
[demo_interfaces](#demo_interfaces-custom-messages) ·
[demo_turtlesim](#demo_turtlesim-drive-the-turtle-from-python) ·
[demo_launch](#demo_launch-launch-files) ·
[demo_tf2](#demo_tf2-frames) ·
[demo_arm_description](#demo_arm_description-the-arm-in-rviz) ·
[demo_arm_gazebo](#demo_arm_gazebo-simulation-and-sensors) ·
[demo_arm_control](#demo_arm_control-ros2_control) ·
[demo_arm_moveit](#demo_arm_moveit-motion-planning) ·
[demo_arm_vision](#demo_arm_vision-opencv-and-pick-and-place) ·
[tests](#tests)

---

## Day 1

### `demo_py`: topics, services, actions, parameters

**Publisher and subscriber**

```bash
# T1
ros2 run demo_py talker            # publishes 'Hello N' on /chatter every 0.5 s (prints nothing)
# T2
ros2 run demo_py listener          # [listener]: I heard: Hello 0, Hello 1, ...
# T3: look from outside
ros2 topic echo /chatter
ros2 topic hz /chatter             # average rate: 2.000
ros2 node info /talker
rqt_graph
```

**Service server and client**

```bash
# T1
ros2 run demo_py add_two_ints_server
# T2
ros2 run demo_py add_two_ints_client                  # sum: 5   (asks for 2 + 3, then exits)
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

**Action server and client**

```bash
# T1
ros2 run demo_py fibonacci_action_server
# T2
ros2 run demo_py fibonacci_action_client              # order 10: feedback once a second, then the result
ros2 run demo_py fibonacci_action_client 4            # ... result: [0, 1, 1, 2, 3]
ros2 action send_goal --feedback fibonacci demo_interfaces/action/Fibonacci "{order: 5}"
# Press Ctrl+C during send_goal to cancel: the server logs the cancel and stops early
```

**Parameters**

```bash
# T1
ros2 run demo_py minimal_param_node --ros-args -p my_parameter:=earth    # Hello earth!
# T2
ros2 param list /minimal_param_node
ros2 param set /minimal_param_node my_parameter mars                     # T1: Hello mars!
ros2 param set /minimal_param_node my_parameter '""'                     # rejected: name is empty
```

**One-command startup: launch + YAML parameters**

```bash
# T1
ros2 launch demo_py demo.launch.py            # rate_talker + listener, rate from config/params.yaml
# T2
ros2 param get /rate_talker rate              # Double value is: 4.0
ros2 topic hz /chatter                        # average rate: 4.000
ros2 param set /rate_talker rate 1.0          # T1: rate is now 1.0 Hz
```

**Timers, executors, logging**

```bash
ros2 run demo_py heartbeat                    # alive, every 0.5 s
ros2 run demo_py executor_demo                # control tick keeps its 0.5 s rhythm while plan runs
ros2 run demo_py logging_demo                 # INFO, WARN, ERROR, FATAL, then a throttled tick
ros2 run demo_py logging_demo --ros-args --log-level debug     # also shows the DEBUG line
ros2 run rqt_console rqt_console              # filter the messages by severity
```

In `demo_py/executor_demo.py`, change `MultiThreadedExecutor` to `SingleThreadedExecutor`,
then run the node again: the control ticks now wait for each slow plan to finish.

### `demo_cpp`: the same in C++

```bash
# Mix languages: they share the same topic and service
ros2 run demo_py talker          # T1
ros2 run demo_cpp listener       # T2: [listener]: I heard: 'Hello 0'

ros2 run demo_cpp talker         # T1
ros2 run demo_py listener        # T2

ros2 run demo_cpp add_two_ints_server          # T1: a: 2 b: 3
ros2 run demo_py add_two_ints_client           # T2: sum: 5

ros2 run demo_cpp param_node --ros-args -p my_parameter:=earth   # Hello earth!
```

After changing a `.cpp` file: `colcon build --packages-select demo_cpp`, then run it again.

### `demo_interfaces`: custom messages

```bash
ros2 interface show demo_interfaces/msg/Num
ros2 interface show demo_interfaces/srv/AddThreeInts
ros2 interface show demo_interfaces/action/Fibonacci

ros2 run demo_py num_publisher                 # T1
ros2 topic echo /num                           # T2: num: 0, num: 1, ... once a second

ros2 run demo_py add_three_ints_server         # T1
ros2 service call /add_three_ints demo_interfaces/srv/AddThreeInts "{a: 1, b: 2, c: 3}"   # sum: 6
```

### `demo_turtlesim`: drive the turtle from Python

Start the simulator first (T1), then run any one node in T2:

```bash
ros2 run turtlesim turtlesim_node                                                  # T1

ros2 run demo_turtlesim draw_circle --ros-args -p linear:=2.0 -p angular:=1.0      # circle radius 2.00 m
ros2 run demo_turtlesim draw_square --ros-args -p side:=4.0                        # corner reached, 3 left ...
ros2 run demo_turtlesim go_to_goal --ros-args -p x:=9.0 -p y:=2.0                  # arrived at (9.0…, 2.0…)
ros2 run demo_turtlesim pose_monitor                                               # logs once on entering or leaving 1 m from a wall
ros2 run demo_turtlesim spawn_turtle --ros-args -p name:=turtle2 -p x:=2.0 -p y:=2.0    # spawned turtle2
ros2 run demo_turtlesim rotate_turtle --ros-args -p theta:=1.57                    # remaining: ... SUCCEEDED
ros2 run demo_turtlesim rotate_turtle --ros-args -p theta:=-1.57 -p cancel_after:=0.5   # CANCELED
ros2 run demo_turtlesim background_color --ros-args -p r:=200 -p g:=86 -p b:=255
ros2 run turtlesim turtle_teleop_key                                               # drive with the arrow keys
```

Or start it all with one command:

```bash
ros2 launch demo_turtlesim turtlesim_demo.launch.py                    # draws a circle
ros2 launch demo_turtlesim turtlesim_demo.launch.py demo:=draw_square
ros2 launch demo_turtlesim turtlesim_demo.launch.py demo:=go_to_goal
```

### `demo_launch`: launch files

```bash
ros2 launch demo_launch namespace.launch.py              # one node in a namespace
ros2 node list                                           # /demo/turtlesim

ros2 launch demo_launch turtles.launch.py --show-args    # arguments and their defaults
ros2 launch demo_launch turtles.launch.py ns:=robot1 background_r:=200

ros2 launch demo_launch turtles.launch.xml               # the same system in XML
ros2 launch demo_launch turtles.launch.yaml ns:=robot1   # ... and in YAML

ros2 launch demo_launch include.launch.py                # includes both, each in a namespace
ros2 node list                                           # /from_xml/turtlesim, /from_yaml/turtlesim

ros2 launch demo_launch params.launch.py                 # parameters from a YAML file
ros2 param get /styled/turtlesim background_b

ros2 launch demo_launch events.launch.py                 # turtle2 spawns on start; close the window to stop all

ros2 launch demo_launch mimic.launch.py                  # T1: two turtlesims, the second copies the first
ros2 topic pub -r 1 /turtlesim1/turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 2.0}, angular: {z: -1.8}}"               # T2
```

---

## Day 2

### `demo_tf2`: frames

**Static frame**

```bash
ros2 run demo_tf2 static_frames                          # T1
ros2 run tf2_ros tf2_echo base_link lidar_link           # T2: Translation: [0.100, 0.000, 0.200]
```

**Broadcaster and listener**

```bash
ros2 run turtlesim turtlesim_node                                               # T1
ros2 run demo_tf2 turtle_frame_publisher --ros-args -p turtlename:=turtle1      # T2
ros2 run demo_tf2 frame_listener --ros-args -p target:=world -p source:=turtle1 # T3: turtle1 at x=5.54 y=5.54
ros2 run turtlesim turtle_teleop_key                                            # T4: drive and watch x, y change
```

**turtle2 follows turtle1**

```bash
ros2 launch demo_tf2 follow.launch.py              # T1
ros2 run turtlesim turtle_teleop_key               # T2: drive turtle1; turtle2 chases it
ros2 run tf2_ros tf2_echo turtle2 turtle1          # T3: the gap the follower steers on
ros2 run tf2_tools view_frames                     # writes frames_*.pdf: the tree world → turtle1, turtle2
```

### `demo_arm_description`: the arm in RViz

```bash
ros2 launch demo_arm_description display.launch.py              # RViz + a joint slider window
ros2 launch demo_arm_description display.launch.py gui:=false   # no slider window

# Check the model from the command line
cd ~/ros2_workshop_code/ros2_ws/src/demo_arm_description/urdf
xacro demo_arm.urdf.xacro > /tmp/demo_arm.urdf && check_urdf /tmp/demo_arm.urdf
xacro examples/two_wheels.urdf.xacro > /tmp/two_wheels.urdf && check_urdf /tmp/two_wheels.urdf
                                                                 # base_link has 2 child(ren)
# With display.launch.py running:
ros2 run tf2_ros tf2_echo base_link tool0                        # where the gripper is
ros2 run tf2_tools view_frames
```

### `demo_arm_gazebo`: simulation and sensors

```bash
ros2 launch demo_arm_gazebo sim.launch.py                   # T1: Gazebo, the arm on a table, controllers
ros2 launch demo_arm_gazebo sim.launch.py rviz:=true        # ... also RViz with the camera and lidar
ros2 launch demo_arm_gazebo sim.launch.py headless:=true    # ... no Gazebo window (slow laptops, SSH)
```

With it running, read every sensor in T2:

```bash
ros2 topic list
ros2 topic hz /camera/camera/color/image_raw                     # RealSense colour
ros2 topic hz /camera/camera/aligned_depth_to_color/image_raw    # RealSense depth
ros2 topic echo /camera/camera/depth/color/points --field header # point cloud
ros2 run rqt_image_view rqt_image_view /camera/camera/color/image_raw
ros2 topic echo /scan --once                                     # lidar
ros2 topic echo /imu --once                                      # IMU in the palm
ros2 topic echo /wrist_ft                                        # force-torque at the wrist
ros2 topic echo /left_finger/contact                             # finger contacts
ros2 topic echo /joint_states --once
```

---

## Day 3

### `demo_arm_control`: ros2_control

Run it with mock hardware (no simulator) or with Gazebo. The commands in T2 are the same
for both.

```bash
ros2 launch demo_arm_control mock.launch.py        # T1, or: ros2 launch demo_arm_gazebo sim.launch.py

ros2 control list_hardware_interfaces              # T2
ros2 control list_controllers                      # 3 controllers active
ros2 run demo_arm_control trajectory_demo          # arm through 4 poses: done, gripper close: done, gripper open: done
ros2 run demo_arm_control gripper close
ros2 run demo_arm_control gripper open
ros2 run demo_arm_control gripper 0.02             # each finger 2 cm from the centre
```

### `demo_arm_moveit`: motion planning

```bash
ros2 launch demo_arm_moveit demo.launch.py                   # mock hardware + MoveIt + RViz
```

In RViz, drag the interactive marker at the gripper, then click **Plan** and **Execute** in
the MotionPlanning panel. Set *Planning Group* to `gripper` to open and close the jaws.

```bash
ros2 launch demo_arm_moveit gazebo.launch.py                 # Gazebo + MoveIt + 3D vision (octomap)
ros2 launch demo_arm_moveit gazebo.launch.py vision:=false   # ... without the camera in the planning scene
ros2 launch demo_arm_moveit gazebo.launch.py headless:=true
```

With `gazebo.launch.py` running, add *PointCloud2* and *Planning Scene* displays in RViz. The
occupancy map built from the RealSense cloud appears, and plans route around it.

### `demo_arm_vision`: OpenCV and pick and place

**Everything with one command**

```bash
ros2 launch demo_arm_vision pick_place_demo.launch.py                     # camera finds the boxes
ros2 launch demo_arm_vision pick_place_demo.launch.py use_vision:=false   # fixed poses from config/params.yaml
ros2 launch demo_arm_vision pick_place_demo.launch.py headless:=true rviz:=false
```

The arm picks the red box, then the blue one, places each in the tray, and logs
`pick and place finished`. Gazebo needs about 20 s to start, so the pick waits that long
(`start_delay:=30.0` gives a slow machine more time).

**Step by step**

```bash
ros2 launch demo_arm_moveit gazebo.launch.py               # T1: simulation + MoveIt
ros2 launch demo_arm_vision vision.launch.py               # T2: detector + planning-scene updater
ros2 topic echo /detections/red                            # T3: box pose in world
ros2 run rqt_image_view rqt_image_view /detections/image   # T3: the image with the detections drawn
```

`pick_and_place` needs the MoveIt settings that MoveItPy reads at start-up, so start it with
`pick_place_demo.launch.py`, not with `ros2 run`.

The HSV ranges, box size, and tray pose are in `demo_arm_vision/config/params.yaml`.
With a real D435, start the camera with
`ros2 launch realsense2_camera rs_launch.py align_depth.enable:=true` instead of Gazebo.

---

## Tests

```bash
cd ~/ros2_workshop_code/ros2_ws
colcon test && colcon test-result --verbose        # flake8, pep257, unit tests, URDF checks
colcon test --packages-select demo_py              # one package
bash scripts/smoke_test.sh                         # run every example briefly
```
