# Everything the workshop needs, for machines without Ubuntu 24.04.
#   docker build -t ros2_workshop -f docker/Dockerfile .
#   bash docker/run.sh
FROM osrf/ros:jazzy-desktop-full

RUN apt-get update && apt-get install -y --no-install-recommends \
      ros-jazzy-ros-gz ros-jazzy-gz-ros2-control \
      ros-jazzy-ros2-control ros-jazzy-ros2-controllers \
      ros-jazzy-xacro ros-jazzy-joint-state-publisher-gui \
      ros-jazzy-moveit ros-jazzy-moveit-py ros-jazzy-pick-ik \
      ros-jazzy-realsense2-description \
      ros-jazzy-cv-bridge python3-opencv \
      ros-jazzy-rqt-image-view ros-jazzy-tf2-tools \
    && rm -rf /var/lib/apt/lists/*

COPY ros2_ws/src /root/ros2_ws/src
RUN . /opt/ros/jazzy/setup.sh && cd /root/ros2_ws \
    && colcon build --symlink-install \
    && echo 'source /opt/ros/jazzy/setup.bash' >> /root/.bashrc \
    && echo 'source /root/ros2_ws/install/setup.bash' >> /root/.bashrc

WORKDIR /root/ros2_ws
