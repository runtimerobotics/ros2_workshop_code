cmake_minimum_required(VERSION 3.10)
project(demo_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generates Python and C++ code for every interface listed here
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Num.msg" "srv/AddThreeInts.srv"
  "action/Fibonacci.action")

ament_export_dependencies(rosidl_default_runtime)
ament_package()
