# Lab 11: find the boxes with OpenCV

**Goal:** turn pixels into a 3D pose in the world frame.

```bash
ros2 launch demo_arm_moveit gazebo.launch.py
ros2 launch demo_arm_vision vision.launch.py            # second terminal

ros2 topic echo /detections/red                         # PoseStamped in world
rqt_image_view /detections/image                        # outlines and coordinates
```

The pipeline in `object_detector.py`:

1. HSV threshold for each colour (`config/params.yaml`), clean with an opening
2. largest blob, its centre `(u, v)` and angle (`cv2.minAreaRect`)
3. median depth around `(u, v)` in the aligned depth image
4. back-project: `x = (u - cx) · z / fx`, `y = (v - cy) · z / fy` (`geometry.py`)
5. TF from `camera_color_optical_frame` to `world`, then half a box down to its centre

Compare with the truth: the red box is at (0.36, 0.10, 0.12) in `worlds/table.sdf`.

**Done when** both detections are within 1 cm of the true positions.

**Challenge:** add a yellow box to `worlds/table.sdf` and a `yellow_ranges` entry to
`params.yaml` (yellow is around H 20–35), then detect it.
