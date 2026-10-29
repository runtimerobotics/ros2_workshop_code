cmake_minimum_required(VERSION 3.10)
project(demo_cpp)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(talker src/talker.cpp)
target_link_libraries(talker rclcpp::rclcpp ${std_msgs_TARGETS})

add_executable(listener src/listener.cpp)
target_link_libraries(listener rclcpp::rclcpp ${std_msgs_TARGETS})

add_executable(add_two_ints_server src/add_two_ints_server.cpp)
target_link_libraries(add_two_ints_server rclcpp::rclcpp ${example_interfaces_TARGETS})

add_executable(param_node src/param_node.cpp)
target_link_libraries(param_node rclcpp::rclcpp)

# Install into lib/demo_cpp so `ros2 run demo_cpp <name>` finds them
install(TARGETS talker listener add_two_ints_server param_node
  DESTINATION lib/${PROJECT_NAME})

ament_package()
