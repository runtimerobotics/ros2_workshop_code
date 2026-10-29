# Lab 0: is this machine ready?

**Goal:** every tool the workshop needs is installed, and two nodes can talk.

Not installed yet? Follow [`setup/README.md`](../setup/README.md) first.

```bash
bash setup/check_setup.sh
echo $ROS_DISTRO                 # jazzy (or lyrical)
ros2 doctor --report | head -30  # look at NETWORK CONFIGURATION and RMW MIDDLEWARE
```

In two terminals:

```bash
ros2 run demo_nodes_cpp talker
ros2 run demo_nodes_py listener
```

**Done when** `check_setup.sh` prints only ✓ lines and the listener prints `I heard: [Hello World: 1]`.

**If nodes cannot see each other:** run `00_linux_basics/scripts/ros_env.sh` in both
terminals; `ROS_DOMAIN_ID` must match. On a shared network, pick your own domain:
`export ROS_DOMAIN_ID=<your seat number>`.
