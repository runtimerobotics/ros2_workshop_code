cmake_minimum_required(VERSION 3.10)
project(demo_arm_moveit)

find_package(ament_cmake REQUIRED)

install(DIRECTORY config launch DESTINATION share/${PROJECT_NAME})

ament_package()
