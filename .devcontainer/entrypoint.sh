#!/bin/bash

set -e
source /opt/ros/humble/setup.bash
cd /pampas

apt update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install \
  --packages-up-to perception control mapper path_planning \
    amp_utils amp_sm depthai_ros_driver amp_bringup yolobot_recognition \

source /pampas/install/setup.bash
exec "$@"
