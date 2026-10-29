# C++ and CMake basics

ROS 2 C++ packages are CMake projects with a few extra lines. Build these first.

```bash
# 1. The smallest CMake project
cd 01_hello_cmake
cmake -S . -B build        # configure: read CMakeLists.txt, write build files
cmake --build build        # compile
./build/hello

# 2. A library, an app that uses it, and a test
cd ../02_robot_lib
cmake -S . -B build && cmake --build build
./build/robot_demo
cd build && ctest --output-on-failure
```

| CMake line | Meaning | ROS 2 equivalent (`demo_cpp`) |
|---|---|---|
| `add_executable(robot_demo app/main.cpp)` | build a program | the same |
| `add_library(robot src/robot.cpp)` | build reusable code | the same |
| `target_link_libraries(robot_demo PRIVATE robot)` | use a library | `target_link_libraries(talker rclcpp::rclcpp ${std_msgs_TARGETS})` |
| `add_test(...)` + `ctest` | run tests | `colcon test` |
| *(none)* | | `install(TARGETS ...)` so `ros2 run` can find it |
