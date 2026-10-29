#!/usr/bin/env bash
# Back up the src folder of a ROS 2 workspace into a dated archive.
# Usage: ./backup_ws.sh [workspace]
set -euo pipefail
ws=${1:-$HOME/ros2_ws}
[[ -d "$ws/src" ]] || { echo "no src folder in $ws" >&2; exit 1; }

out="$HOME/ws_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$out" -C "$ws" src
echo "saved $(du -h "$out" | cut -f1) to $out"
