#!/usr/bin/env bash
# Variables, arguments, if, and for.
# Usage: ./hello.sh Ada 3
name=${1:-robot}          # first argument, or "robot" if none was given
count=${2:-2}

if [[ "$count" -gt 5 ]]; then
  echo "That is a lot of greetings, $name."
fi

for i in $(seq 1 "$count"); do
  echo "Hello $name, number $i"
done
