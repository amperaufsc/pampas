cmake_minimum_required(VERSION 3.8)
project(amp_msgs)

find_package(ament_cmake REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/SteeringActuatorControlDebug.msg"
  DEPENDENCIES std_msgs
)

ament_package()
