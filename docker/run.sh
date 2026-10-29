#!/usr/bin/env bash
# Start the workshop container with a window display (Linux, X11).
# The workspace is mounted from this repository, so edits on the host show up inside.
set -e
cd "$(dirname "$0")/.."
xhost +local:root >/dev/null 2>&1 || true
docker run -it --rm \
  --net=host --ipc=host \
  -e DISPLAY="$DISPLAY" -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$PWD/ros2_ws/src:/root/ros2_ws/src" \
  --device /dev/dri \
  ros2_workshop bash
