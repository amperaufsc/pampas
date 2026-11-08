cmake_minimum_required(VERSION 3.8)
project(amp_control)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# The argument to ament_python_install_package() is the name of the directory
# alongside the CMakeLists.txt that contains the Python file.
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  ros2/motion_control_node.py
  ros2/motion_control_node_life.py
  ros2/actuator_control_node.py
  ros2/actuator_control_node_sim.py
  ros2/ros_can_publisher.py
  ros2/mouse_control_node.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
