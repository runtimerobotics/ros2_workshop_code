#!/usr/bin/env bash
# Show the ROS environment of this terminal: the first thing to check when
# "command not found" or "nodes cannot see each other".
echo "ROS_DISTRO      = ${ROS_DISTRO:-<not set: source /opt/ros/jazzy/setup.bash>}"
echo "ROS_DOMAIN_ID   = ${ROS_DOMAIN_ID:-0 (default)}"
echo "RMW             = ${RMW_IMPLEMENTATION:-default (rmw_fastrtps_cpp)}"
echo "LOCALHOST_ONLY  = ${ROS_AUTOMATIC_DISCOVERY_RANGE:-SUBNET (default)}"
echo "AMENT_PREFIX_PATH:"
tr ':' '\n' <<< "${AMENT_PREFIX_PATH:-}" | sed 's/^/  /'
