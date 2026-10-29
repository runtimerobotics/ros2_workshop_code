# Lab 4: request and goal

**Goal:** know when to use a service (short request, one reply) and when an action
(a goal that takes time, with feedback and cancel).

Services:

```bash
ros2 run demo_py add_two_ints_server          # or: ros2 run demo_cpp add_two_ints_server
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
ros2 run demo_py add_two_ints_client 4 5      # sum: 9, without blocking the node

ros2 run demo_py add_three_ints_server        # your own .srv
ros2 service call /add_three_ints demo_interfaces/srv/AddThreeInts "{a: 1, b: 2, c: 3}"
```

Actions:

```bash
ros2 run demo_py fibonacci_action_server
ros2 run demo_py fibonacci_action_client 8                     # feedback every second
ros2 action send_goal --feedback fibonacci demo_interfaces/action/Fibonacci "{order: 10}"
#   press Ctrl+C during the goal: the server reports it canceled
```

With turtlesim:

```bash
ros2 run turtlesim turtlesim_node
ros2 run demo_turtlesim spawn_turtle --ros-args -p name:=turtle2        # services
ros2 run demo_turtlesim rotate_turtle --ros-args -p theta:=3.14          # action
ros2 run demo_turtlesim rotate_turtle --ros-args -p theta:=-1.57 -p cancel_after:=0.5
ros2 run demo_turtlesim background_color --ros-args -p r:=200            # parameters
```

**Done when** you can explain why spawning is a service and rotating is an action.

**Challenge:** write a client for `/add_three_ints` (start from `add_two_ints_client.py`).
