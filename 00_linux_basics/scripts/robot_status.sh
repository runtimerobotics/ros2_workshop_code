#!/usr/bin/env bash
# Read a battery level from a file and decide what the robot should do.
# Usage: ./robot_status.sh [battery_file]
battery_file=${1:-/tmp/battery.txt}
[[ -f "$battery_file" ]] || echo 72 > "$battery_file"   # create a fake reading the first time

level=$(cat "$battery_file")
echo "battery: ${level}%"

if   [[ "$level" -le 20 ]]; then echo "status: LOW, return to dock"; exit 1
elif [[ "$level" -le 50 ]]; then echo "status: OK, finish the current task"
else                             echo "status: GOOD, ready for a new task"
fi
