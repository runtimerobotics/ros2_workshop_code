# Lab 13: capstone

Put the three days together and report the evidence.

1. **Launch** the robot and world with one command.
2. **Verify** the graph (`rqt_graph`), the frames (`view_frames`), the controllers
   (`ros2 control list_controllers`), and every sensor rate (`ros2 topic hz`).
3. **Add** an obstacle the planner does not know about, and a target pose.
4. **Plan, execute,** and report: the planning time, the trajectory duration, and the
   final pose error from `tf2_echo world tool0`.

Submit: a frame diagram, the controller states, sensor rates, and one screenshot of RViz
with the occupancy map and the planned path.

Ideas for a stretch:

- stack the blue box on the red one
- pick a box that is rotated 30° (change its yaw in `table.sdf`)
- run the detector on a real RealSense: `ros2 launch realsense2_camera rs_launch.py align_depth.enable:=true`
