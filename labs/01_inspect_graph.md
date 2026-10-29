# Lab 1: inspect a running graph

**Goal:** explain every node, topic, service, and action of turtlesim, and draw the graph.

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key           # second terminal: drive with the arrow keys

ros2 node list
ros2 topic list -t
ros2 service list -t
ros2 action list -t
ros2 node info /turtlesim
ros2 topic info /turtle1/pose --verbose        # publisher, QoS: RELIABLE, VOLATILE
ros2 topic hz /turtle1/pose                    # about 62.5 Hz
rqt_graph
```

**Done when** you can point at each arrow in `rqt_graph` and say which message type flows on it.

**Challenge:** run `ros2 topic echo /turtle1/pose` with
`--qos-reliability best_effort`. Does it still receive? Why? (Best effort can listen to reliable.)
