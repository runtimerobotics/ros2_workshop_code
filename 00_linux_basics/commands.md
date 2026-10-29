# Linux commands for the workshop

Every command here is used somewhere in the labs. Try each one in a terminal.

## Where am I, and what is here?
| Command | What it does |
|---|---|
| `pwd` | print the current directory |
| `ls -la` | list files, including hidden ones, with details |
| `cd ~/ros2_ws/src` | change directory (`~` is your home, `..` is one level up, `-` is the previous one) |
| `tree -L 2` | show a folder tree two levels deep (`sudo apt install tree`) |

## Files and folders
| Command | What it does |
|---|---|
| `mkdir -p ~/ros2_ws/src` | create a folder and any missing parents |
| `touch notes.txt` | create an empty file |
| `nano talker.py` | edit a file in the terminal (Ctrl+O save, Ctrl+X quit) |
| `cat file` / `less file` | print a file / page through it (`q` quits) |
| `cp a.py b.py` | copy |
| `mv b.py talker.py` | move or rename |
| `rm a.py` / `rm -r folder` | delete: there is no bin, it is gone |

## Find things
| Command | What it does |
|---|---|
| `grep -rn "create_publisher" src/` | search inside files, with line numbers |
| `find . -name "*.launch.py"` | find files by name |
| `which ros2` | where a command lives |
| `history \| grep colcon` | search commands you ran before |

## Processes
| Command | What it does |
|---|---|
| `Ctrl+C` | stop the program running in this terminal |
| `ps aux \| grep turtlesim` | list running processes |
| `kill <pid>` / `pkill -f turtlesim` | stop a process by id / by name |
| `htop` | live view of CPU and memory |

## Permissions
| Command | What it does |
|---|---|
| `chmod +x script.sh` | make a script executable |
| `./script.sh` | run it from the current folder |
| `sudo apt install <pkg>` | install software as administrator |

## Environment variables (ROS uses these a lot)
| Command | What it does |
|---|---|
| `echo $ROS_DISTRO` | print one variable |
| `printenv \| grep ROS` | list all ROS variables |
| `export ROS_DOMAIN_ID=7` | set a variable for this terminal only |
| `source /opt/ros/jazzy/setup.bash` | run a script in this shell, so its variables stay |
| `echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc` | do it in every new terminal |

## Tips
- `Tab` completes names; press it twice to see the choices.
- `↑` brings back the previous command.
- Every new terminal starts fresh: source ROS (and your workspace) again, or put it in `~/.bashrc`.
