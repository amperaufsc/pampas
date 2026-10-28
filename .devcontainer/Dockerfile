# syntax=docker/dockerfile:1

# ---------- Stage 1: package.xml manifests only ----------
# Lets the rosdep layer cache until a package.xml actually changes.
FROM ros:humble AS manifests
COPY src /src
RUN find /src -type f ! -name package.xml -delete

# ---------- Stage 2: main image ----------
FROM ros:humble

USER root
SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

# Keep downloaded .debs so the apt cache mounts are useful
RUN rm -f /etc/apt/apt.conf.d/docker-clean \
    && echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' \
       > /etc/apt/apt.conf.d/keep-cache

# All system packages in ONE layer, before any COPY
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    # ROS tools / GUI
    ros-humble-rqt ros-humble-rqt-common-plugins \
    qt6-wayland bash-completion \
    # build tools
    cmake g++ ninja-build python3-dev python3-pip \
    # Pangolin
    libgl1-mesa-dev libegl1-mesa-dev libwayland-dev libxkbcommon-dev \
    wayland-protocols libc++-dev libepoxy-dev libglew-dev libeigen3-dev \
    libjpeg-dev libpng-dev libopenexr-dev catch2 \
    libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev \
    libdc1394-dev libraw1394-dev libopenni-dev \
    # ORB_SLAM3
    libopencv-dev libboost-all-dev

RUN python3 -m pip install --no-cache-dir wheel setuptools

# Third-party deps live OUTSIDE /pampas so the bind mount can't hide them
WORKDIR /opt/deps

# Pangolin (installs to /usr/local)
COPY src/Pangolin ./Pangolin
RUN cd Pangolin \
    && cmake -B build -GNinja \
    && cmake --build build -j"$(nproc)" \
    && cmake --install build \
    && ldconfig \
    && rm -rf build

# ORB_SLAM3 (build.sh also extracts Vocabulary/ORBvoc.txt)
COPY src/ORB_SLAM3 ./ORB_SLAM3
RUN cd ORB_SLAM3 && ./build.sh \
    && printf '%s\n' \
       /opt/deps/ORB_SLAM3/lib \
       /opt/deps/ORB_SLAM3/Thirdparty/DBoW2/lib \
       /opt/deps/ORB_SLAM3/Thirdparty/g2o/lib \
       > /etc/ld.so.conf.d/orbslam3.conf \
    && ldconfig
ENV ORB_SLAM3_ROOT_DIR=/opt/deps/ORB_SLAM3

# Python deps (rebuilds only when pyproject/uv.lock change)
COPY --from=ghcr.io/astral-sh/uv:latest@sha256:8b7774a14bb3abde914fda03efcb83f1f7e9163124e5c13e7fb4cc825293f5fa /uv /uvx /bin/
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /pampas
# venv can see system ROS packages (rclpy)
RUN uv venv --system-site-packages /opt/venv
COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project

# ROS deps (rebuilds only when a package.xml changes)
COPY --from=manifests /src /tmp/src
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && rosdep update \
    && rosdep install -y --ignore-src --from-paths \
       $(colcon list --base-paths /tmp/src --paths-only --packages-up-to \
         perception control mapper path_planning amp_utils amp_sm \
         depthai_ros_driver amp_bringup yolobot_recognition orbslam3_ros2) \
    && rm -rf /tmp/src

# Shell setup
RUN cat >> /root/.bashrc <<'EOF'
source /opt/ros/humble/setup.bash
[ -f /pampas/install/setup.bash ] && source /pampas/install/setup.bash
alias ls='ls --color=auto'
alias grep='grep --color=auto'
EOF

COPY .devcontainer/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
