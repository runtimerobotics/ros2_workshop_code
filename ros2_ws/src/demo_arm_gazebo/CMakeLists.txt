cmake_minimum_required(VERSION 3.10)
project(demo_arm_gazebo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY worlds config launch rviz DESTINATION share/${PROJECT_NAME})
install(PROGRAMS scripts/points_frame_fix.py DESTINATION lib/${PROJECT_NAME})

ament_package()
