#!/usr/bin/env bash
# Install ROS 2 Lyrical Luth on Ubuntu 26.04 (resolute).
# The workshop labs target Jazzy; use this to try the newest LTS.
set -euo pipefail

if [[ "$(. /etc/os-release && echo "$VERSION_CODENAME")" != "resolute" ]]; then
  echo "ROS 2 Lyrical needs Ubuntu 26.04 (resolute). For Ubuntu 24.04 use ROS 2 Jazzy." >&2
  exit 1
fi

sudo apt update && sudo apt install -y locales software-properties-common curl
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
sudo add-apt-repository -y universe

ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb \
  "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo "$VERSION_CODENAME")_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

sudo apt update && sudo apt upgrade -y
sudo apt install -y ros-lyrical-desktop ros-dev-tools

grep -qxF 'source /opt/ros/lyrical/setup.bash' ~/.bashrc || echo 'source /opt/ros/lyrical/setup.bash' >> ~/.bashrc
echo "Done. Open a new terminal and run: echo \$ROS_DISTRO   # lyrical"
