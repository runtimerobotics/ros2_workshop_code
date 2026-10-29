# Lab 3: write and run your own nodes

**Goal:** a publisher and a subscriber in Python and in C++, talking across languages,
and your own message type.

```bash
ros2 run demo_py talker
ros2 run demo_cpp listener            # Python → C++: same message, any language

ros2 run demo_cpp talker
ros2 run demo_py listener             # C++ → Python

ros2 run demo_py num_publisher        # the custom demo_interfaces/msg/Num
ros2 interface show demo_interfaces/msg/Num
ros2 topic echo /num
```

Read the code side by side: `demo_py/demo_py/talker.py` and `demo_cpp/src/talker.cpp`.
The timer, the publisher, and the message are the same ideas in both.

Change something and see it without rebuilding Python (`--symlink-install`):
edit the message text in `talker.py`, stop the node, run it again.
C++ needs `colcon build --packages-select demo_cpp` first.

**Done when** both directions work and you can say which line creates the publisher in each language.

**Challenge:** add a field `string label` to `Num.msg`, rebuild `demo_interfaces` and
`demo_py`, and publish it from `num_publisher`.
