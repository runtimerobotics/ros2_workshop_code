# Lab 5: one-command startup

**Goal:** start a configured system with one command, and change it without editing code.

```bash
ros2 launch demo_py demo.launch.py                  # rate_talker + listener
ros2 param get /rate_talker rate                    # 4.0, from config/params.yaml
ros2 topic hz /chatter
ros2 param set /rate_talker rate 1.0                # changes the timer while running
```

Edit `demo_py/config/params.yaml` (rate, prefix) and launch again: with
`--symlink-install` there is nothing to rebuild.

The same node in three formats, and composition:

```bash
ros2 launch demo_launch turtles.launch.py --show-args
ros2 launch demo_launch turtles.launch.py ns:=robot1 background_r:=200
ros2 launch demo_launch turtles.launch.xml
ros2 launch demo_launch turtles.launch.yaml ns:=robot1
ros2 launch demo_launch include.launch.py           # includes the XML and the YAML file
ros2 launch demo_launch mimic.launch.py             # one turtle copies another
ros2 launch demo_launch events.launch.py            # close the window: everything stops
```

**Done when** you can change the talker's rate from YAML and see it with `ros2 topic hz`.

**Challenge:** add a `ns` launch argument to `demo.launch.py` and start two copies side by side.
