# Set up your computer

Do this before Day 1. It takes 30 to 60 minutes, mostly downloads. You need internet and a
user that can run `sudo`.

## 1. Get Ubuntu

| Your computer | Do this |
|---|---|
| Ubuntu 24.04 already | go to step 2 (you will use ROS 2 Jazzy) |
| Ubuntu 26.04 already | go to step 2 (you will use ROS 2 Lyrical) |
| Windows or macOS, or another Linux | install Ubuntu 24.04 next to it (dual boot), or in a virtual machine with at least 8 GB memory, 4 CPU cores, 40 GB disk, and 3D acceleration on. Or skip to [the Docker option](#docker-instead) |

The workshop teaches Jazzy. Lyrical works the same; where a command says `jazzy`, write `lyrical`.

## 2. Get the code

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/runtimerobotics/ros2_workshop_code.git ~/ros2_workshop_code
cd ~/ros2_workshop_code
```

## 3. Install ROS 2 and the lab packages

```bash
bash setup/install_jazzy.sh          # Ubuntu 24.04
bash setup/install_lyrical.sh        # Ubuntu 26.04 (instead of the line above)
```

The script stops with a message if your Ubuntu does not match. It:

1. sets a UTF-8 locale and turns on Ubuntu's `universe` repository
2. adds the ROS 2 apt repository (`ros2-apt-source`)
3. upgrades the system, then installs `ros-<distro>-desktop` and `ros-dev-tools` (colcon, rosdep)
4. installs the lab packages: Gazebo (`ros-gz`), `ros2_control` and its controllers,
   `gz_ros2_control`, `xacro`, MoveIt 2 with `moveit_py` and `pick_ik`, the RealSense model, and OpenCV
5. sets up `rosdep`
6. adds `source /opt/ros/<distro>/setup.bash` to `~/.bashrc`

**Open a new terminal** when it finishes, so `~/.bashrc` runs.

## 4. Check the machine

```bash
cd ~/ros2_workshop_code
bash setup/check_setup.sh
```

Every line should start with ✓ and the last line should be `14 passed, 0 failed`. A ✗ line
names what is missing; the table below says what to do.

## 5. Build the workshop workspace

```bash
cd ~/ros2_workshop_code/ros2_ws
rosdep install --from-paths src -y --ignore-src
colcon build --symlink-install
echo "source ~/ros2_workshop_code/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

`colcon build` ends with `Summary: 11 packages finished`.

## 6. Try it

```bash
ros2 run demo_py talker            # terminal 1
ros2 run demo_cpp listener         # terminal 2: I heard: 'Hello 0', 'Hello 1', ...
ros2 launch demo_arm_gazebo sim.launch.py      # the arm in Gazebo (close with Ctrl+C)
```

Optional, about 5 minutes: `bash scripts/smoke_test.sh` in `ros2_ws` runs every example and
should print `13 passed, 0 failed`.

Every command for every example is in [`ros2_ws/README.md`](../ros2_ws/README.md).

## If something goes wrong

| You see | Do this |
|---|---|
| `ros2: command not found` | open a new terminal, or run `source /opt/ros/jazzy/setup.bash` |
| `Package 'demo_py' not found` | run `source ~/ros2_workshop_code/ros2_ws/install/setup.bash`, or build first (step 5) |
| `Could not read the ros-apt-source release from api.github.com` | your network blocks the GitHub API. Look up the newest version at <https://github.com/ros-infrastructure/ros-apt-source/releases>, then run `ROS_APT_SOURCE_VERSION=1.3.0 bash setup/install_jazzy.sh` with that version |
| `Unable to locate package ros-jazzy-...` | the ROS apt repository is missing or your Ubuntu is not 24.04: check `lsb_release -a`, then run the install script again |
| `ERROR: default sources list file already exists` (rosdep) | harmless: rosdep was set up before |
| ✗ `talker → listener` in `check_setup.sh` | a firewall or another ROS computer on the network. Try `export ROS_DOMAIN_ID=42` (any number 0–101, the same in every terminal), and on a shared network `export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` |
| Gazebo is black, crashes, or is very slow (often in a virtual machine) | `export LIBGL_ALWAYS_SOFTWARE=1` before launching, or run without a window: `ros2 launch demo_arm_gazebo sim.launch.py headless:=true` |
| `colcon build` runs out of memory | `colcon build --symlink-install --parallel-workers 1` |
| Ctrl+C on Lyrical sometimes prints an `RCLError` traceback | harmless: a callback was running while ROS shut down |

## Docker instead

On a Linux computer that has Docker but not Ubuntu 24.04 or 26.04:

```bash
cd ~/ros2_workshop_code
docker build -t ros2_workshop -f docker/Dockerfile .      # add --build-arg ROS_DISTRO=lyrical for Lyrical
bash docker/run.sh                                        # opens a shell inside, with windows shown on your screen
```

See [`docker/README.md`](../docker/README.md).

## Is the setup tested?

Yes. [`install.yml`](../.github/workflows/install.yml) runs both install scripts on a plain
Ubuntu 24.04 and 26.04, then steps 4 and 5, every week and whenever `setup/` changes.
[`ci.yml`](../.github/workflows/ci.yml) builds, tests, and runs every example on both releases
on every push.
