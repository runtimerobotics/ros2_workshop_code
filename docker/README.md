# Docker

For machines without Ubuntu 24.04 or 26.04, or to try the other ROS 2 release. Linux with X11 shows Gazebo and RViz windows directly.

```bash
docker build -t ros2_workshop -f docker/Dockerfile .                                 # ROS 2 Jazzy
# or: docker build -t ros2_workshop --build-arg ROS_DISTRO=lyrical -f docker/Dockerfile .   # ROS 2 Lyrical
bash docker/run.sh
# inside the container
colcon build --symlink-install && source install/setup.bash
ros2 launch demo_arm_vision pick_place_demo.launch.py
```

No display (a server or CI)? Gazebo and the sensors still run:

```bash
ros2 launch demo_arm_vision pick_place_demo.launch.py headless:=true rviz:=false
```
