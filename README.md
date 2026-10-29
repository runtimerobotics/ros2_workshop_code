# ROS 2 Workshop Code

[![build and test](https://github.com/runtimerobotics/ros2_workshop_code/actions/workflows/ci.yml/badge.svg)](https://github.com/runtimerobotics/ros2_workshop_code/actions/workflows/ci.yml)
[![ROS 2 Jazzy](https://img.shields.io/badge/ROS_2-Jazzy-22314E?logo=ros)](https://docs.ros.org/en/jazzy/)
[![ROS 2 Lyrical](https://img.shields.io/badge/ROS_2-Lyrical-22314E?logo=ros)](https://docs.ros.org/en/lyrical/)
[![Ubuntu 24.04 | 26.04](https://img.shields.io/badge/Ubuntu-24.04_%7C_26.04-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com/download/desktop)
[![Gazebo Harmonic | Jetty](https://img.shields.io/badge/Gazebo-Harmonic_%7C_Jetty-F58113)](https://gazebosim.org/docs)
[![MoveIt 2](https://img.shields.io/badge/MoveIt-2-1F6FB5)](https://moveit.picknik.ai/)
[![Python | C++](https://img.shields.io/badge/code-Python_%7C_C%2B%2B-3776AB?logo=python&logoColor=white)](ros2_ws/README.md)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Slides](https://img.shields.io/badge/slides-open-00A3A3)](https://runtimerobotics.github.io/ros2_workshop_slides/)

Everything you type, run, and change during the three-day ROS 2 workshop, from the first
Linux command to a robot arm that finds a box with a camera and places it in a tray.
The same code runs on **ROS 2 Jazzy (Ubuntu 24.04)**, the release the workshop teaches, and on
**ROS 2 Lyrical (Ubuntu 26.04)**. CI builds, tests, and runs every example on both.

Slides: <https://runtimerobotics.github.io/ros2_workshop_slides/>

![The arm, the table, and the overhead RealSense](docs/images/demo_arm.png)

## What is inside

| Folder or package | Day | What you learn |
|---|---|---|
| [`setup/`](setup) | before | install ROS 2 Jazzy (or Lyrical), check the machine is ready |
| [`00_linux_basics/`](00_linux_basics) | prerequisites | terminal commands and shell scripts |
| [`01_python_basics/`](01_python_basics) | prerequisites | the Python a ROS node uses: classes and callbacks |
| [`02_cpp_cmake_basics/`](02_cpp_cmake_basics) | prerequisites | C++ with CMake: a program, a library, a test |
| [`demo_interfaces`](ros2_ws/src/demo_interfaces) | 1 | custom message, service, and action |
| [`demo_py`](ros2_ws/src/demo_py) | 1 | topics, services, actions, parameters, timers, executors in Python |
| [`demo_cpp`](ros2_ws/src/demo_cpp) | 1 | the same in C++, built with CMake |
| [`demo_turtlesim`](ros2_ws/src/demo_turtlesim) | 1 | drive, draw, spawn, rotate, and recolour turtles from Python |
| [`demo_launch`](ros2_ws/src/demo_launch) | 1 | launch files in Python, XML, and YAML |
| [`demo_tf2`](ros2_ws/src/demo_tf2) | 2 | static and moving frames, lookups, a turtle that follows another |
| [`demo_arm_description`](ros2_ws/src/demo_arm_description) | 2 | URDF/Xacro of a 5-joint arm with a gripper and sensors |
| [`demo_arm_gazebo`](ros2_ws/src/demo_arm_gazebo) | 2 | Gazebo world, RealSense, lidar, IMU, force-torque, contact sensors |
| [`demo_arm_control`](ros2_ws/src/demo_arm_control) | 3 | ros2_control controllers, trajectories without a planner |
| [`demo_arm_moveit`](ros2_ws/src/demo_arm_moveit) | 3 | MoveIt 2: planning, IK, straight-line moves, 3D vision |
| [`demo_arm_vision`](ros2_ws/src/demo_arm_vision) | 3 | find coloured boxes with OpenCV, pick and place with MoveItPy |
| [`labs/`](labs) | all | one page per lab: goal, commands, what "done" looks like |

## The robot: `demo_arm`

An RRBot-style arm: box links in RRBot's orange and black, five revolute joints
(base yaw, shoulder, elbow, wrist pitch, wrist roll) and a two-jaw gripper, about 0.7 m reach.

| Sensor | Where | ROS topic |
|---|---|---|
| Intel RealSense D435 (RGB-D) | on a stand, looking down at the table | `/camera/camera/color/image_raw`, `/camera/camera/aligned_depth_to_color/image_raw`, `/camera/camera/depth/color/points` |
| 2D lidar | front of the pedestal | `/scan` |
| IMU | gripper palm | `/imu` |
| Force-torque | wrist roll joint | `/wrist_ft` |
| Contact | both fingers | `/left_finger/contact`, `/right_finger/contact` |
| Joint encoders | every joint | `/joint_states` |

The camera topics use the same names as the real `realsense2_camera` driver, so the
vision code also runs on a real D435 (`ros2 launch realsense2_camera rs_launch.py align_depth.enable:=true`).

## Prerequisites

**Computer**

| | Minimum | Recommended |
|---|---|---|
| CPU | 4 cores, x86-64 or ARM64 | 8 cores |
| Memory | 8 GB | 16 GB (Gazebo, MoveIt, and RViz together) |
| Disk | 20 GB free | 40 GB |
| Graphics | any; `headless:=true` runs Gazebo without a window | a GPU with OpenGL 3.3 for smooth Gazebo and RViz |
| Network | internet for the install | the same for every machine in a multi-robot lab |

**Operating system and ROS 2**, pick one row:

| Ubuntu | ROS 2 | Gazebo | Python | Install script |
|---|---|---|---|---|
| 24.04 LTS (Noble) | Jazzy Jalisco (LTS, used in the workshop) | Harmonic | 3.12 | [`setup/install_jazzy.sh`](setup/install_jazzy.sh) |
| 26.04 LTS (Resolute) | Lyrical Luth (LTS) | Jetty | 3.14 | [`setup/install_lyrical.sh`](setup/install_lyrical.sh) |

Windows or macOS: use a virtual machine with Ubuntu, or the container in [`docker/`](docker).
WSL 2 on Windows 11 can work too (WSLg shows the Gazebo and RViz windows), but it is not tested here.

**Packages** (the install script installs all of them):

| Package | Used for |
|---|---|
| `ros-<distro>-desktop`, `ros-dev-tools` | ROS 2, RViz, rqt, turtlesim, colcon, rosdep |
| `ros-<distro>-ros-gz` | Gazebo and the ROS–Gazebo bridge |
| `ros-<distro>-ros2-control`, `ros-<distro>-ros2-controllers`, `ros-<distro>-gz-ros2-control` | controllers, in Gazebo and with mock hardware |
| `ros-<distro>-xacro`, `ros-<distro>-joint-state-publisher-gui` | the robot model |
| `ros-<distro>-moveit`, `ros-<distro>-moveit-py`, `ros-<distro>-pick-ik` | motion planning, its Python API, and the IK solver |
| `ros-<distro>-realsense2-description` | the RealSense D435 model |
| `ros-<distro>-cv-bridge`, `python3-opencv` | box detection with OpenCV |

**What you should know first:** opening a terminal, `cd`, and `ls`, and enough Python to read a
class. The [`00_linux_basics/`](00_linux_basics), [`01_python_basics/`](01_python_basics), and
[`02_cpp_cmake_basics/`](02_cpp_cmake_basics) folders cover the rest before Day 1.

## Setup

```bash
git clone https://github.com/runtimerobotics/ros2_workshop_code.git
cd ros2_workshop_code
bash setup/install_jazzy.sh          # Ubuntu 24.04: ROS 2 Jazzy, Gazebo, ros2_control, MoveIt, OpenCV
# bash setup/install_lyrical.sh      # Ubuntu 26.04: the same for ROS 2 Lyrical
bash setup/check_setup.sh            # every line should start with ✓ (finds Jazzy or Lyrical)

source /opt/ros/jazzy/setup.bash     # Lyrical: /opt/ros/lyrical/setup.bash (the install script adds it to ~/.bashrc)
cd ros2_ws
rosdep install --from-paths src -y --ignore-src
colcon build --symlink-install
source install/setup.bash            # in every new terminal, or add it to ~/.bashrc
```

No Ubuntu 24.04 or 26.04? Use the container in [`docker/`](docker), which builds either release.

## Quick start

A taste of each day. The full list is in [`ros2_ws/README.md`](ros2_ws/README.md).

```bash
# Day 1: two nodes talking
ros2 run demo_py talker
ros2 run demo_cpp listener                         # second terminal: Python → C++

# Day 1: one command, a configured system
ros2 launch demo_turtlesim turtlesim_demo.launch.py demo:=draw_square

# Day 2: the arm in RViz, then in Gazebo with its sensors
ros2 launch demo_arm_description display.launch.py
ros2 launch demo_arm_gazebo sim.launch.py rviz:=true

# Day 3: MoveIt without a simulator, then the full pick and place
ros2 launch demo_arm_moveit demo.launch.py
ros2 launch demo_arm_vision pick_place_demo.launch.py
ros2 launch demo_arm_vision pick_place_demo.launch.py use_vision:=false   # fixed box poses
```

## Run the examples

Step-by-step commands, with the output to expect:

| Guide | Covers |
|---|---|
| [`00_linux_basics/`](00_linux_basics/README.md) | terminal commands and the shell scripts |
| [`01_python_basics/`](01_python_basics/README.md) | `python3 01_basics.py` … the exercise and its checks |
| [`02_cpp_cmake_basics/`](02_cpp_cmake_basics/README.md) | `cmake` configure, build, run, and `ctest` |
| [**`ros2_ws/README.md`**](ros2_ws/README.md) | **every ROS 2 node and launch file, package by package, Day 1 to Day 3** |
| [`labs/`](labs/README.md) | the workshop labs: goal, commands, what "done" looks like |
| [`docker/`](docker/README.md) | the same, inside a container |

## How pick and place works

```
RealSense colour + depth ──▶ object_detector ──▶ /detections/red, /detections/blue (poses in world)
                                   │ OpenCV: HSV threshold → largest blob → depth at its centre
                                   │ → back-project with the camera intrinsics → TF to world
RealSense point cloud ──▶ move_group occupancy map (OctoMap): unknown obstacles are avoided
pick_and_place (MoveItPy):
   home → open → pre-grasp (OMPL) → straight down (Pilz LIN) → attach + close
   → straight up → over the tray → straight down → detach + open → straight up → home
```

In Gazebo, a box is locked to the palm while it is held (`DetachableJoint`), because
friction grasps of small boxes slip in simulation; MoveIt attaches it in its planning scene
at the same moment. With `use_vision:=false` the boxes come from `config/params.yaml`.

## Jazzy and Lyrical: what differs

One source tree builds and runs on both releases. These are the places where Lyrical changed
something, and how the code handles them:

| Change in Lyrical | What the code does (works on both) |
|---|---|
| `ament_target_dependencies()` was removed from CMake | `target_link_libraries(talker rclcpp::rclcpp ${std_msgs_TARGETS})` in [`demo_cpp`](ros2_ws/src/demo_cpp/CMakeLists.txt) |
| turtlesim's message, service, and action types moved to `turtlesim_msgs` | `try: from turtlesim_msgs.msg import Pose` / `except ImportError: from turtlesim.msg import Pose` |
| rclpy's `logger.warn()` was removed | `logger.warning()` |
| Ctrl+C raises `ExternalShutdownException` instead of `KeyboardInterrupt` | `except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):` in every `main()` |
| controllers with mock hardware no longer receive the controller manager's parameter file | the spawner gets `--param-file` in each launch file |
| `flake8-class-newline` is part of the style tests | a blank line after each `class ...:` line |
| Gazebo Jetty replaces Harmonic | nothing: the world, sensors, and bridge are the same |

On Lyrical, Ctrl+C sometimes prints an `RCLError` traceback from a callback that was running
during shutdown. rclpy's own demo nodes do the same; it is harmless.

## Tests

```bash
cd ros2_ws
colcon test && colcon test-result --verbose
```

Every Python package runs flake8 and pep257; `demo_py`, `demo_turtlesim`, and
`demo_arm_vision` have unit tests for their plain functions; `demo_arm_description` checks
that every variant of the URDF expands. On every push, CI builds and tests everything and runs
[`scripts/smoke_test.sh`](ros2_ws/scripts/smoke_test.sh) on Jazzy and on Lyrical.

## Licence

Apache-2.0. The RealSense model comes from Intel's
[`realsense2_description`](https://github.com/IntelRealSense/realsense-ros) (Apache-2.0).
The arm's look follows RRBot from [`ros2_control_demos`](https://github.com/ros-controls/ros2_control_demos).
