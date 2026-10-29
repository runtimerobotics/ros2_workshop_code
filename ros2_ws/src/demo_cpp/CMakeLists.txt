cmake_minimum_required(VERSION 3.8)
project(demo_cpp)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(talker src/talker.cpp)
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/listener.cpp)
ament_target_dependencies(listener rclcpp std_msgs)

add_executable(add_two_ints_server src/add_two_ints_server.cpp)
ament_target_dependencies(add_two_ints_server rclcpp example_interfaces)

add_executable(param_node src/param_node.cpp)
ament_target_dependencies(param_node rclcpp)

# Install into lib/demo_cpp so `ros2 run demo_cpp <name>` finds them
install(TARGETS talker listener add_two_ints_server param_node
  DESTINATION lib/${PROJECT_NAME})

ament_package()
