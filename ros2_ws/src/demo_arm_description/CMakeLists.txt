cmake_minimum_required(VERSION 3.10)
project(demo_arm_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf launch rviz DESTINATION share/${PROJECT_NAME})   # urdf/ includes examples/

if(BUILD_TESTING)
  # every variant of the model must expand and parse
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_urdf test/test_urdf.py)
endif()

ament_package()
