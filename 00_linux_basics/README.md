# Linux basics

- [`commands.md`](commands.md): every command the labs use, with one line on what it does.
- [`navigate_exercise.sh`](navigate_exercise.sh): the "Navigate the file system" slide as a script; it runs in a temporary folder.
- [`scripts/`](scripts): small shell scripts to read and change.

| Script | Shows |
|---|---|
| `hello.sh Ada 3` | variables, arguments with defaults, `if`, `for` |
| `robot_status.sh` | reading a file, `if`/`elif`, exit codes |
| `backup_ws.sh` | `set -euo pipefail`, `tar`, dates in file names |
| `ros_env.sh` | the ROS environment variables to check first when something is wrong |

```bash
cd 00_linux_basics
chmod +x scripts/*.sh       # once
./scripts/hello.sh Ada 3
```
