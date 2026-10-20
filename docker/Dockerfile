FROM ros:humble

USER root
WORKDIR /pampas
SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-rqt ros-humble-rqt-common-plugins \
    qt6-wayland bash-completion \
    ninja-build libegl1-mesa-dev libc++-dev libavdevice-dev \
    ament-cmake libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# --- uv ---
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
# venv can see system ROS packages (rclpy)
RUN uv venv --system-site-packages /opt/venv
# dependency layer: only rebuilds when these files change
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-install-project

# Pangolin
COPY src/Pangolin ./src/Pangolin
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-dev libwayland-dev libxkbcommon-dev wayland-protocols libegl1-mesa-dev \
    libc++-dev libepoxy-dev libglew-dev libeigen3-dev cmake g++ ninja-build \
    libjpeg-dev libpng-dev libopenexr-dev catch2 \
    libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev \
    libdc1394-dev libraw1394-dev libopenni-dev python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install wheel setuptools
RUN cd src/Pangolin \
    && cmake -B build -GNinja && cmake --build build \
    && cmake --install build/ && ldconfig \
    && rm -rf /var/lib/apt/lists/*

# ORB_SLAM3
COPY src/ORB_SLAM3 ./src/ORB_SLAM3
RUN apt-get update && apt-get install -y --no-install-recommends \
    libboost-all-dev
RUN cd src/ORB_SLAM3 \
    && ./build.sh

# ORB_SLAM3 ROS package
COPY src/orbslam3_ros2 ./src/orbslam3_ros2
RUN source /opt/ros/humble/setup.bash \
    && colcon build --symlink-install --packages-select orbslam3_ros2
# Extract ORB vocabulary
RUN cd /pampas/install/orbslam3_ros2/share/orbslam3_ros2/vocabulary/ \
    && tar -xzf ORBvoc.txt.tar.gz

# Build workspace
# COPY src ./src
# RUN apt-get update && rosdep update \
#     && rosdep install --from-paths /pampas/src --ignore-src -r -y \
#     && rm -rf /var/lib/apt/lists/*

# RUN source /opt/ros/humble/setup.bash \
#     && colcon build --packages-up-to \
#     perception control mapper path_planning amp_utils amp_sm \
#     depthai_ros_driver amp_bringup yolobot_recognition

RUN echo 'source /opt/ros/humble/setup.bash' >> /root/.bashrc \
    && echo "alias ls='ls --color=auto'; alias grep='grep --color=auto'" >> \
    /root/.bashrc
    # && echo 'PS1="\[\e[32m\]\u@\h\[\e[0m\]:\[\e[34m\]\w\[\e[0m\]\$ "' >> /root/.bashrc

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
