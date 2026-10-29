#!/usr/bin/env bash
# Install ROS 2 Lyrical Luth and everything the workshop labs need on Ubuntu 26.04.
# Usage: bash setup/install_lyrical.sh
set -euo pipefail

if [[ "$(. /etc/os-release && echo "$VERSION_CODENAME")" != "resolute" ]]; then
  echo "ROS 2 Lyrical needs Ubuntu 26.04 (resolute). For Ubuntu 24.04 use ROS 2 Jazzy." >&2
  exit 1
fi

echo "== 1-2. Locale and universe repository"
sudo apt update && sudo apt install -y locales software-properties-common curl
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
sudo add-apt-repository -y universe

echo "== 3. ROS 2 apt source"
# The newest ros-apt-source release. If api.github.com is blocked, look it up at
# https://github.com/ros-infrastructure/ros-apt-source/releases and run: ROS_APT_SOURCE_VERSION=1.x.x bash <this script>
ROS_APT_SOURCE_VERSION=${ROS_APT_SOURCE_VERSION:-$(curl -s ${GITHUB_TOKEN:+-H "Authorization: Bearer $GITHUB_TOKEN"} \
  https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}' || true)}
[[ -n "$ROS_APT_SOURCE_VERSION" ]] || { echo "Could not read the ros-apt-source release from api.github.com (see the comment above)." >&2; exit 1; }
curl -fL -o /tmp/ros2-apt-source.deb \
  "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo "$VERSION_CODENAME")_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

echo "== 4. ROS 2 desktop and developer tools"
sudo apt update && sudo apt upgrade -y
sudo apt install -y ros-lyrical-desktop ros-dev-tools

echo "== 5. Packages for the Day 2 and Day 3 labs"
# Required for the Day 2 and Day 3 labs
sudo apt install -y ros-lyrical-ros-gz ros-lyrical-gz-ros2-control \
  ros-lyrical-ros2-control ros-lyrical-ros2-controllers \
  ros-lyrical-xacro ros-lyrical-joint-state-publisher-gui \
  ros-lyrical-moveit ros-lyrical-moveit-py ros-lyrical-pick-ik \
  ros-lyrical-realsense2-description ros-lyrical-cv-bridge python3-opencv

echo "== 6. rosdep"
[[ -f /etc/ros/rosdep/sources.list.d/20-default.list ]] || sudo rosdep init
rosdep update

grep -qxF 'source /opt/ros/lyrical/setup.bash' ~/.bashrc || echo 'source /opt/ros/lyrical/setup.bash' >> ~/.bashrc
echo "Done. Open a new terminal, then run: bash setup/check_setup.sh"
