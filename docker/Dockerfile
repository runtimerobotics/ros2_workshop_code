# Everything the workshop needs, for machines without Ubuntu 24.04 or 26.04.
#   docker build -t ros2_workshop -f docker/Dockerfile .                               # Jazzy
#   docker build -t ros2_workshop --build-arg ROS_DISTRO=lyrical -f docker/Dockerfile . # Lyrical
#   bash docker/run.sh
ARG ROS_DISTRO=jazzy
FROM osrf/ros:${ROS_DISTRO}-desktop-full
ARG ROS_DISTRO

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
      ros-${ROS_DISTRO}-ros-gz ros-${ROS_DISTRO}-gz-ros2-control \
      ros-${ROS_DISTRO}-ros2-control ros-${ROS_DISTRO}-ros2-controllers \
      ros-${ROS_DISTRO}-xacro ros-${ROS_DISTRO}-joint-state-publisher-gui \
      ros-${ROS_DISTRO}-moveit ros-${ROS_DISTRO}-moveit-py ros-${ROS_DISTRO}-pick-ik \
      ros-${ROS_DISTRO}-realsense2-description \
      ros-${ROS_DISTRO}-cv-bridge python3-opencv \
      ros-${ROS_DISTRO}-rqt-image-view ros-${ROS_DISTRO}-tf2-tools \
    && rm -rf /var/lib/apt/lists/*

COPY ros2_ws/src /root/ros2_ws/src
RUN . /opt/ros/${ROS_DISTRO}/setup.sh && cd /root/ros2_ws \
    && colcon build --symlink-install \
    && echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc \
    && echo 'source /root/ros2_ws/install/setup.bash' >> /root/.bashrc

WORKDIR /root/ros2_ws
