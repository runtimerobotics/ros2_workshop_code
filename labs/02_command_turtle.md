# Lab 2: command the turtle

**Goal:** publish velocity from the command line, then from your own Python node.

```bash
ros2 run turtlesim turtlesim_node
ros2 interface show geometry_msgs/msg/Twist

# a circle: radius = linear.x / angular.z = 1.25 m
ros2 topic pub --rate 2 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.5}, angular: {z: 1.2}}"
```

Now the same from Python, then closed-loop control:

```bash
ros2 run demo_turtlesim draw_circle --ros-args -p linear:=2.0 -p angular:=1.0
ros2 run demo_turtlesim go_to_goal --ros-args -p x:=9.0 -p y:=2.0
ros2 run demo_turtlesim pose_monitor            # warns near a wall
```

Read `demo_turtlesim/demo_turtlesim/go_to_goal.py`: it subscribes to `/turtle1/pose`,
computes the heading error, and publishes `/turtle1/cmd_vel` 20 times a second.

**Done when** the turtle stops within 5 cm of the goal and logs `arrived`.

**Challenge:** `draw_square` visits four corners. Make it draw a triangle
(start from `square_corners()` and its test in `test/test_geometry.py`).
