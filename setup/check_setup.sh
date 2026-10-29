#!/usr/bin/env bash
# Check that a machine is ready for the workshop. Prints one line per check.
# Usage: bash setup/check_setup.sh
source /opt/ros/jazzy/setup.bash 2>/dev/null || { echo "✗ /opt/ros/jazzy not found: run setup/install_jazzy.sh"; exit 1; }

pass=0; fail=0
check() {   # check "description" command...
  if "${@:2}" >/dev/null 2>&1; then echo "✓ $1"; pass=$((pass + 1)); else echo "✗ $1"; fail=$((fail + 1)); fi
}

check "ROS_DISTRO is jazzy"            test "$ROS_DISTRO" = jazzy
check "ros2 command works"             ros2 --help
check "colcon installed"               command -v colcon
check "rosdep installed"               command -v rosdep
check "turtlesim installed"            ros2 pkg prefix turtlesim
check "Gazebo bridge (ros_gz) installed" ros2 pkg prefix ros_gz_bridge
check "ros2_control installed"         ros2 pkg prefix controller_manager
check "gz_ros2_control installed"      ros2 pkg prefix gz_ros2_control
check "MoveIt 2 installed"             ros2 pkg prefix moveit_ros_move_group
check "moveit_py installed"            python3 -c "import moveit"
check "RealSense description installed" ros2 pkg prefix realsense2_description
check "OpenCV for Python installed"    python3 -c "import cv2"

# A talker and a listener must see each other.
timeout 6 ros2 run demo_nodes_cpp talker >/dev/null 2>&1 &
if timeout 5 ros2 topic echo --once /chatter >/dev/null 2>&1; then echo "✓ talker → listener works"; pass=$((pass + 1)); else echo "✗ talker → listener: check ROS_DOMAIN_ID and firewall"; fail=$((fail + 1)); fi
wait 2>/dev/null

echo "$pass passed, $fail failed"
[[ $fail -eq 0 ]]
