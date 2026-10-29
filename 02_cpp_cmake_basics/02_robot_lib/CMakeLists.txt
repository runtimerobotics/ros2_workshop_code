cmake_minimum_required(VERSION 3.16)
project(robot_lib CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# A library: code other targets can use
add_library(robot src/robot.cpp)
target_include_directories(robot PUBLIC include)

# An executable that links the library
add_executable(robot_demo app/main.cpp)
target_link_libraries(robot_demo PRIVATE robot)

# A test, run with ctest
enable_testing()
add_executable(test_robot test/test_robot.cpp)
target_link_libraries(test_robot PRIVATE robot)
add_test(NAME test_robot COMMAND test_robot)
