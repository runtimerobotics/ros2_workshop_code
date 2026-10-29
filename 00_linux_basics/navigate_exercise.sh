#!/usr/bin/env bash
# The "Navigate the file system" exercise, step by step. Run it and read along.
# It works in a temporary folder, so it never touches your real files.
set -euo pipefail
cd "$(mktemp -d)"
say() { printf '\n$ %s\n' "$*"; "$@"; }

say mkdir -p ros2_ws/src
say cd ros2_ws/src
echo "print('hello')" > a.py; echo; echo "$ nano a.py      # (here we just write print('hello') into it)"
say cp a.py b.py
say mv b.py talker.py
say ls -la
say rm a.py
say cd ..
say pwd
say cat src/talker.py
