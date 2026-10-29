#!/usr/bin/env bash
# Run each example briefly and check its output. Used by CI; also handy after a change:
#   source install/setup.bash && bash scripts/smoke_test.sh
# Set SKIP_SIM=1 to leave out the Gazebo pick-and-place run (about 3 minutes).
set -u
export QT_QPA_PLATFORM=offscreen RCUTILS_LOGGING_BUFFERED_STREAM=0 PYTHONUNBUFFERED=1
pass=0; fail=0
ok() { echo "✓ $1"; pass=$((pass + 1)); }
bad() { echo "✗ $1"; fail=$((fail + 1)); }
expect() {   # expect "description" "pattern" seconds command...: run until the pattern appears
  local what=$1 pattern=$2 secs=$3 log; shift 3
  log=$(mktemp)
  timeout -s INT "$secs" "$@" > "$log" 2>&1 &
  local pid=$! found=0
  for _ in $(seq $((secs * 4))); do
    if grep -q -E "$pattern" "$log"; then found=1; break; fi
    kill -0 $pid 2>/dev/null || break
    sleep 0.25
  done
  grep -q -E "$pattern" "$log" && found=1
  pkill -INT -P $pid 2>/dev/null; kill -INT $pid 2>/dev/null; wait $pid 2>/dev/null
  if [[ $found == 1 ]]; then ok "$what"; else bad "$what"; tail -5 "$log" | sed 's/^/    /'; fi
  rm -f "$log"
}
bg() { (timeout -s INT "$1" "${@:2}" > /dev/null 2>&1 &); }
cleanup() { pkill -INT -f "[t]urtlesim_node|[d]emo_py|[d]emo_cpp|[r]os2 launch" 2>/dev/null; sleep 2; }

echo "== Day 1: topics, services, actions, parameters"
bg 8 ros2 run demo_py talker;  expect "Python talker → C++ listener" "I heard: 'Hello" 6 ros2 run demo_cpp listener; cleanup
bg 8 ros2 run demo_cpp talker; expect "C++ talker → Python listener" "I heard: Hello" 6 ros2 run demo_py listener; cleanup
bg 8 ros2 run demo_cpp add_two_ints_server; sleep 2
expect "service: 4 + 5" "sum: 9" 6 ros2 run demo_py add_two_ints_client 4 5; cleanup
bg 15 ros2 run demo_py fibonacci_action_server; sleep 2
expect "action: Fibonacci with feedback" "result: \[0, 1, 1, 2, 3\]" 12 ros2 run demo_py fibonacci_action_client 4; cleanup
bg 12 ros2 run demo_py minimal_param_node; sleep 3
expect "parameter validation" "name is empty" 8 ros2 param set /minimal_param_node my_parameter '""'; cleanup
bg 12 ros2 launch demo_py demo.launch.py; sleep 4
expect "launch + YAML parameters" "Double value is: 4.0" 5 ros2 param get /rate_talker rate; cleanup

echo "== Day 1: turtlesim"
bg 20 ros2 run turtlesim turtlesim_node; sleep 2
expect "go_to_goal arrives" "arrived" 15 ros2 run demo_turtlesim go_to_goal --ros-args -p x:=9.0 -p y:=2.0
expect "spawn service" "spawned turtle2" 8 ros2 run demo_turtlesim spawn_turtle
expect "rotate action" "SUCCEEDED" 10 ros2 run demo_turtlesim rotate_turtle --ros-args -p theta:=1.57; cleanup
bg 12 ros2 launch demo_launch include.launch.py; sleep 5
expect "launch XML + YAML includes" "/from_yaml/turtlesim" 5 ros2 node list; cleanup

echo "== Day 2: tf2"
bg 8 ros2 run demo_tf2 static_frames; sleep 2
expect "static transform" "Translation: \[0.150, 0.000, 0.120\]" 6 ros2 run tf2_ros tf2_echo base_link camera_link; cleanup

echo "== Day 3: ros2_control and MoveIt with mock hardware"
bg 60 ros2 launch demo_arm_moveit demo.launch.py rviz:=false; sleep 15
expect "trajectory through the controllers" "arm through 4 poses: done" 40 ros2 run demo_arm_control trajectory_demo; cleanup

if [[ "${SKIP_SIM:-0}" != 1 ]]; then
  echo "== Day 3: Gazebo, vision, and pick and place (headless)"
  expect "pick and place with vision" "pick and place finished" 400 \
    ros2 launch demo_arm_vision pick_place_demo.launch.py headless:=true rviz:=false start_delay:=30.0
  cleanup; pkill -9 -f "[g]z sim" 2>/dev/null
fi

echo "$pass passed, $fail failed"
[[ $fail -eq 0 ]]
