# Lab 8: spawn the arm in Gazebo and read every sensor

**Goal:** the arm in a simulated world, every sensor publishing at its rate, in the right frame.

```bash
ros2 launch demo_arm_gazebo sim.launch.py rviz:=true
```

Check each sensor: type, rate, frame.

```bash
ros2 topic list -t | grep -E "camera|scan|imu|wrist|contact"
ros2 control list_controllers                           # three active: the arm can move
ros2 topic hz /camera/camera/color/image_raw            # 30 Hz at real time
ros2 topic echo --once /camera/camera/color/camera_info # fx, fy, cx, cy
ros2 topic hz /scan                                     # 10 Hz
ros2 topic echo --once /imu
ros2 topic echo /wrist_ft                               # changes when the arm moves
ros2 topic echo /left_finger/contact                    # only while touching something
ros2 run tf2_ros tf2_echo world camera_color_optical_frame
```

Compare simulation time and wall time:

```bash
ros2 topic echo --once /clock
gz topic -e -t /stats -n 1 | grep real_time_factor
```

**Done when** you can name, for each sensor, its topic, its message type, its rate, and its frame.

**Challenge:** change the lidar to 720 samples and 20 Hz in `gazebo.xacro`, rebuild,
and measure the new rate.

**Challenge:** raise the lidar noise in `gazebo.xacro` from `0.01` to `0.05` m, rebuild,
and compare the scan of the table legs in RViz: the points spread out.
